/*
 * Copyright 2015-2018 Mikkel Strange, Fawzi Mohamed, Ankit Kariryaa, Ask Hjorth Larsen, Jens Jørgen Mortensen
 * 
 *   Licensed under the Apache License, Version 2.0 (the "License");
 *   you may not use this file except in compliance with the License.
 *   You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 *   Unless required by applicable law or agreed to in writing, software
 *   distributed under the License is distributed on an "AS IS" BASIS,
 *   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *   See the License for the specific language governing permissions and
 *   limitations under the License.
 */

package eu.nomad_lab.parsers
import eu.{ nomad_lab => lab }
import org.{ json4s => jn }
import scala.collection.breakOut

object GpawParser2 extends SimpleExternalParserGenerator(
  name = "GpawParser2",
  parserInfo = jn.JObject(
    ("name" -> jn.JString("GpawParser2")) ::
      ("parserId" -> jn.JString("GpawParser2" + lab.GpawVersionInfo.version)) ::
      ("versionInfo" -> jn.JObject(
        ("nomadCoreVersion" -> jn.JObject(lab.NomadCoreVersionInfo.toMap.map {
          case (k, v) => k -> jn.JString(v.toString)
        }(breakOut): List[(String, jn.JString)])) ::
          (lab.GpawVersionInfo.toMap.map {
            case (key, value) =>
              (key -> jn.JString(value.toString))
          }(breakOut): List[(String, jn.JString)])
      )) :: Nil
  ),
  // output file is binary and first 16 bytes is a string containing: 'GPAW'
  // In python the check is like this
  // is_gpw_file = 'GPAW' in str(open('file.gpw', 'rb').read(16))
  // How do we do this in scala?
  mainFileTypes = Seq("application/x-bin"),
  mainFileRe = "- of UlmGPAW|AFFormatGPAW".r,
  cmd = Seq(lab.DefaultPythonInterpreter.pythonExe(), "${envDir}/parsers/gpaw/parser/parser-gpaw/parser2.py",
    "${mainFilePath}"),
  resList = Seq(
    "parser-gpaw/parser2.py",
    "parser-gpaw/default_parameters.py",
    "parser-gpaw/libxc_names.py",
    "parser-gpaw/setup_paths.py",
    "nomad_meta_info/public.nomadmetainfo.json",
    "nomad_meta_info/common.nomadmetainfo.json",
    "nomad_meta_info/meta.nomadmetainfo.json",
    "nomad_meta_info/gpaw.nomadmetainfo.json"
  ) ++ lab.DefaultPythonInterpreter.commonFiles(),
  dirMap = Map(
    "parser-gpaw" -> "parsers/gpaw/parser/parser-gpaw",
    "nomad_meta_info" -> "nomad-meta-info/meta_info/nomad_meta_info"
  ) ++ lab.DefaultPythonInterpreter.commonDirMapping()
) {
  override def isMainFile(filePath: String, bytePrefix: Array[Byte], stringPrefix: Option[String]): Option[ParserMatch] = {
    if (filePath.endsWith(".gpw"))
      Some(ParserMatch(mainFileMatchPriority, mainFileMatchWeak))
    else
      None
  }
}
