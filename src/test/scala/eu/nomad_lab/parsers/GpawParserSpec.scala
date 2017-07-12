package eu.nomad_lab.parsers

import org.specs2.mutable.Specification

object GpawParserSpec extends Specification {
  "GpawParserTest" >> {
    "H2 test with json-events" >> {
      ParserRun.parse(GpawParser, "parsers/gpaw/test/examples/H2.gpw", "json-events") must_== ParseResult.ParseSuccess
    }
    "H2 test with json" >> {
      ParserRun.parse(GpawParser, "parsers/gpaw/test/examples/H2.gpw", "json") must_== ParseResult.ParseSuccess
    }
    "Fe2 test with json-events" >> {
      ParserRun.parse(GpawParser, "parsers/gpaw/test/examples/Fe2.gpw", "json-events") must_== ParseResult.ParseSuccess
    }
    "Fe2 test with json" >> {
      ParserRun.parse(GpawParser, "parsers/gpaw/test/examples/Fe2.gpw", "json") must_== ParseResult.ParseSuccess
    }
    "Au test with json-events" >> {
      ParserRun.parse(GpawParser2, "parsers/gpaw/test/examples/Au.fcc.ulm.gpw", "json-events") must_== ParseResult.ParseSuccess
    }
    "Au test with json" >> {
      ParserRun.parse(GpawParser2, "parsers/gpaw/test/examples/Au.fcc.ulm.gpw", "json") must_== ParseResult.ParseSuccess
    }
  }
}
