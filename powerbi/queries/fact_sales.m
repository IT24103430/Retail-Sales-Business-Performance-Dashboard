// Query name: FactSales. Create all four dimension queries before this query.
let
    Folder = Text.TrimEnd(Text.Trim(DataFolder), {"\", "/"}) & "\",
    Source = Csv.Document(
        File.Contents(Folder & "fact_sales.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Columns = {
        "SalesLineID", "OrderID", "OrderDate", "ProductID", "CustomerID",
        "RegionID", "ChannelID", "Quantity", "UnitPrice", "UnitCost", "DiscountAmount"
    },
    Selected = Table.SelectColumns(Headers, Columns),
    Trimmed = Table.TransformColumns(
        Selected,
        List.Transform(Columns, (column) => {
            column,
            each let value = Text.Trim(_) in if value = "" then null else value,
            type text
        })
    ),
    // Parse ISO dates explicitly and decimal points independently of Windows locale.
    ParsedDates = Table.TransformColumns(
        Trimmed,
        {{"OrderDate", each Date.FromText(_, [Format = "yyyy-MM-dd", Culture = "en-US"]), type date}}
    ),
    Typed = Table.TransformColumnTypes(
        ParsedDates,
        {
            {"Quantity", type number},
            {"UnitPrice", Currency.Type},
            {"UnitCost", Currency.Type},
            {"DiscountAmount", Currency.Type}
        },
        "en-US"
    ),
    WithoutErrors = Table.RemoveRowsWithErrors(Typed),
    RequiredValues = Table.SelectRows(
        WithoutErrors,
        each List.NonNullCount(Record.FieldValues(_)) = List.Count(Columns)
    ),
    // Check quantity before converting to Whole Number so fractions are not rounded.
    ValidRows = Table.SelectRows(
        RequiredValues,
        each [Quantity] > 0 and [Quantity] = Number.RoundDown([Quantity])
            and [UnitPrice] > 0 and [UnitCost] >= 0 and [UnitCost] < [UnitPrice]
            and [DiscountAmount] >= 0
            and [DiscountAmount] <= [Quantity] * [UnitPrice]
            and [OrderDate] >= #date(2025, 1, 1)
            and [OrderDate] <= #date(2026, 9, 30)
    ),
    WholeQuantity = Table.TransformColumnTypes(ValidRows, {{"Quantity", Int64.Type}}),
    ValidQuantity = Table.RemoveRowsWithErrors(WholeQuantity, {"Quantity"}),
    DistinctRows = Table.Distinct(ValidQuantity),
    UniqueLines = if Table.RowCount(DistinctRows) =
        Table.RowCount(Table.Distinct(DistinctRows, {"SalesLineID"}))
        then DistinctRows
        else error "Conflicting SalesLineID values in fact_sales.csv. Review the data profile.",
    // Inner joins remove unmatched keys. Nested results are not expanded.
    MatchedProducts = Table.NestedJoin(
        UniqueLines, {"ProductID"}, DimProducts, {"ProductID"}, "_Product", JoinKind.Inner
    ),
    // Match both keys so the fact region also agrees with the customer's region.
    MatchedCustomers = Table.NestedJoin(
        MatchedProducts, {"CustomerID", "RegionID"},
        DimCustomers, {"CustomerID", "RegionID"}, "_Customer", JoinKind.Inner
    ),
    MatchedRegions = Table.NestedJoin(
        MatchedCustomers, {"RegionID"}, DimRegions, {"RegionID"}, "_Region", JoinKind.Inner
    ),
    MatchedChannels = Table.NestedJoin(
        MatchedRegions, {"ChannelID"}, DimChannels, {"ChannelID"}, "_Channel", JoinKind.Inner
    ),
    CleanRows = Table.RemoveColumns(MatchedChannels, {"_Product", "_Customer", "_Region", "_Channel"}),
    AddedGrossSales = Table.AddColumn(
        CleanRows, "GrossSales", each [Quantity] * [UnitPrice], Currency.Type
    ),
    AddedNetSales = Table.AddColumn(
        AddedGrossSales, "NetSales", each [GrossSales] - [DiscountAmount], Currency.Type
    ),
    AddedTotalCost = Table.AddColumn(
        AddedNetSales, "TotalCost", each [Quantity] * [UnitCost], Currency.Type
    ),
    AddedLineProfit = Table.AddColumn(
        AddedTotalCost, "LineProfit", each [NetSales] - [TotalCost], Currency.Type
    )
in
    AddedLineProfit
