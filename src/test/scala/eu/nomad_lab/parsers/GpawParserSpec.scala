/*
   Copyright 2016-2017 The NOMAD Developers Group

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
 */
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
