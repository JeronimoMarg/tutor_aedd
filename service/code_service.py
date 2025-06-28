from pathlib import Path
import subprocess
import tempfile

from repository.environment import Environment

class CodeService(object):
    def __init__(self, env: Environment):
        self.cpp_version = env.CPP_VERSION

    def compile_cpp(self, source_file: str, output_file: str = "a.out") -> tuple[bool, str]:
        source_path = Path(source_file)
        if not source_path.exists():
            return False, f"Archivo no encontrado: {source_file}"

        cmd = ["g++", str(source_file), "-std=" + self.cpp_version, "-o", output_file]
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False  # No lanza excepción si falla
            )
            if result.returncode == 0:
                return True, result.stdout or "Compilación exitosa."
            else:
                return False, result.stderr
        except Exception as e:
            return False, f"Error al ejecutar el compilador: {e}"
        
    def compile_code_from_text(self, code_text: str, output_file: str = "a.out") -> tuple[bool, str]:
        # Guardar el codigo en un archivo temporal
        with tempfile.NamedTemporaryFile(mode="w", suffix=".cpp", delete=False) as tmp:
            tmp.write(code_text)
            tmp_path = tmp.name

        success, message = self.compile_cpp(tmp_path, output_file)
        # eliminar el archivo temporal
        Path(tmp_path).unlink(missing_ok=True)

        return success, message