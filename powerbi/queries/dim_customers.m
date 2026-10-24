// Query name: DimCustomers. DataFolder must point to the project's data\raw folder.
let
    Folder = Text.TrimEnd(Text.Trim(DataFolder), {"\", "/"}) & "\",
    Source = Csv.Document(
        File.Contents(Folder & "dim_customers.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Columns = {"CustomerID", "CustomerLabel", "CustomerSegment", "RegionID"},
    Selected = Table.SelectColumns(Headers, Columns),
    // Trim every label and key, including Category where present; blank text becomes null.
    Trimmed = Table.TransformColumns(
        Selected,
        List.Transform(Columns, (column) => {
            column,
            each let value = Text.Trim(_) in if value = "" then null else value,
            type text
        })
    ),
    WithoutErrors = Table.RemoveRowsWithErrors(Trimmed),
    ValidRows = Table.SelectRows(
        WithoutErrors,
        each List.NonNullCount(Record.FieldValues(_)) = List.Count(Columns)
    ),
    // Remove identical copies, but stop if one key describes conflicting records.
    DistinctRows = Table.Distinct(ValidRows),
    UniqueKeys = if Table.RowCount(DistinctRows) =
        Table.RowCount(Table.Distinct(DistinctRows, {"CustomerID"}))
        then DistinctRows
        else error "Conflicting CustomerID values in dim_customers.csv. Review the data profile.",
    // Remove customers whose region is missing from the cleaned region dimension.
    MatchedRegions = Table.NestedJoin(
        UniqueKeys, {"RegionID"}, DimRegions, {"RegionID"}, "_Region", JoinKind.Inner
    ),
    Result = Table.RemoveColumns(MatchedRegions, {"_Region"})
in
    Result
