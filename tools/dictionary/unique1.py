import locale
from pathlib import Path

# Set Swedish locale (may require system locale to be installed)
try:
    locale.setlocale(locale.LC_COLLATE, 'sv_SE.UTF-8')
except locale.Error:
    print("Warning: Swedish locale 'sv_SE.UTF-8' is not installed on your system.")
    print("Sorting might not be accurate without it.")

def read_lines(file_path: Path) -> list[str]:
    return [line.strip() for line in file_path.read_text(encoding="utf-8").splitlines() if line.strip()]

def remove_exact_duplicates(lines: list[str]) -> list[str]:
    seen = set()
    result = []
    for line in lines:
        if line not in seen:
            result.append(line)
            seen.add(line)
    return result

def remove_partial_duplicates(lines: list[str]) -> list[str]:
    result = []
    skip_indices = set()
    for i, line in enumerate(lines):
        if i in skip_indices:
            continue
        for j in range(i + 1, len(lines)):
            other = lines[j]
            if line[:5] == other[:5]:
                shorter, longer = (line, other) if len(line) < len(other) else (other, line)
                if shorter[:-2] in longer:
                    skip_indices.add(i if shorter == line else j)
        if i not in skip_indices:
            result.append(line)
    return result

def swedish_sort(lines: list[str]) -> list[str]:
    return sorted(lines, key=locale.strxfrm)

def process_file(input_path: Path, output_path: Path):
    lines = read_lines(input_path)
    lines = remove_exact_duplicates(lines)
    lines = remove_partial_duplicates(lines)
    lines = swedish_sort(lines)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Processed {input_path} -> {output_path}")

# Example usage
input_file = Path("words.txt")
output_file = Path("words_unique_sorted.txt")
process_file(input_file, output_file)
