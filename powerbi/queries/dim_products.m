// Query name: DimProducts. DataFolder must point to the project's data\raw folder.
let
    Folder = Text.TrimEnd(Text.Trim(DataFolder), {"\", "/"}) & "\",
    Source = Csv.Document(
        File.Contents(Folder & "dim_products.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
    Columns = {"ProductID", "ProductName", "Category"},
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
        Table.RowCount(Table.Distinct(DistinctRows, {"ProductID"}))
        then DistinctRows
        else error "Conflicting ProductID values in dim_products.csv. Review the data profile."
in
    UniqueKeys
