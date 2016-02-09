package eu.nomad_lab.parsers
import eu.nomad_lab.DefaultPythonInterpreter
import org.{json4s => jn}

object GpawParser extends SimpleExternalParserGenerator(
  name = "GpawParser",
  parserInfo = jn.JObject(
    ("name" -> jn.JString("GpawParser")) ::
      ("version" -> jn.JString("1.0")) :: Nil),
  mainFileTypes = Seq("application/x-gtar"),
  mainFileRe = "".r,
  cmd = Seq(DefaultPythonInterpreter.python2Exe(), "${envDir}/parsers/gpaw/parser/parser-gpaw/parser.py",
    "${mainFilePath}"),
  resList = Seq(
    "parser-gpaw/parser.py",
    "parser-gpaw/tar.py",
    "parser-gpaw/setup_paths.py",
    "nomad_meta_info/common.nomadmetainfo.json",
    "nomad_meta_info/meta_types.nomadmetainfo.json",
    "nomad_meta_info/gpaw.nomadmetainfo.json"
  ) ++ DefaultPythonInterpreter.commonFiles(),
  dirMap = Map(
    "parser-gpaw" -> "parsers/gpaw/parser/parser-gpaw",
    "nomad_meta_info" -> "nomad-meta-info/meta_info/nomad_meta_info"
  ) ++ DefaultPythonInterpreter.commonDirMapping()
) {
  override def isMainFile(filePath: String, bytePrefix: Array[Byte], stringPrefix: Option[String]): Option[ParserMatch] = {
   if (filePath.endsWith(".gpw"))
      Some(ParserMatch(mainFileMatchPriority, mainFileMatchWeak))
   else
      None
  }
}
