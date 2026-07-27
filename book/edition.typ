#let edition = json("edition.json")
#assert(edition.schema_version == 1, message: "unsupported edition contract schema")

#let stack-lines(values) = {
  for (index, value) in values.enumerate() {
    if index > 0 {
      linebreak()
    }
    value
  }
}
