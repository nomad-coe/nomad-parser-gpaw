package eu.nomad_lab.parsers

import org.specs2.mutable.Specification



object GpawParserSpec extends Specification {
  "GpawParserTest" >> {
    "test with json-events" >> {
      ParserRun.parse(GpawParser, "parsers/gpaw/test/examples/H2.gpw", "json-events") must_== ParseResult.ParseSuccess
    }
    "test with json" >> {
      ParserRun.parse(GpawParser, "parsers/gpaw/test/examples/H2.gpw", "json") must_== ParseResult.ParseSuccess
    }
  }
}
