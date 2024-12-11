
class Parser:
    def __init__(self, file_path):
        """
        Inicjalizuje parser z podaną ścieżką do pliku.

        :param file_path: Ścieżka do pliku .sol (smart contract)
        """
        if not file_path.endswith(".sol"):
            raise ValueError("Plik musi mieć rozszerzenie .sol")
        self.file_path = file_path

    def read_contract(self):
        """
        Odczytuje zawartość smart kontraktu.

        :return: Zawartość pliku jako string
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Plik {self.file_path} nie został znaleziony.")

    def extract_functions(self):
        """
        Ekstrahuje wszystkie funkcje ze smart kontraktu.

        :return: Lista funkcji (każda funkcja jako string)
        """
        contract_code = self.read_contract()
        functions = []
        lines = contract_code.splitlines()

        inside_function = False
        brace_count = 0
        current_function = []

        for line in lines:
            line = line.strip()

            if line.startswith("function ") and not inside_function:
                inside_function = True
                current_function = [line]
                brace_count = line.count("{") - line.count("}")

            elif inside_function:
                current_function.append(line)
                brace_count += line.count("{") - line.count("}")

                if brace_count == 0:
                    inside_function = False
                    functions.append("\n".join(current_function))
                    current_function = []

        return functions


if __name__ == "__main__":
    FILE_PATH = "../../data/example.sol"
    parser = Parser(FILE_PATH)
    functions = parser.extract_functions()

    for i, func in enumerate(functions):
        print(f"Funkcja {i + 1}:\n{func}\n")
