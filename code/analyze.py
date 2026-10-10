import subprocess
import csv
import os

def get_data(path):
    cmd = ["hdfs", "dfs", "-cat", path]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    counts = []
    for line in proc.stdout:
        line = line.decode("utf-8", errors="ignore").strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) == 2 and parts[1].isdigit():
            counts.append((parts[0], int(parts[1])))
    return counts

def export_to_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Word", "Count"])
        for word, count in data:
            writer.writerow([word, count])
    print("  Successfully exported CSV: {}".format(filename))

t1 = get_data("/user/root/output/part-r-00000")
t2 = get_data("/user/root/task2_output/part-00000")

t1_sorted = sorted(t1, key=lambda x: x[1], reverse=True)
t2_sorted = sorted(t2, key=lambda x: x[1], reverse=True)

print("=== TASK 1 (Raw Java WordCount) ===")
print("Total Unique Tokens :", len(t1))
print("Total Word Occurrences:", sum(c for _, c in t1))
print("\nTop 15 Most Frequent Tokens in Task 1:")
for w, c in t1_sorted[:15]:
    print("  {:<15} : {}".format(w, c))

print("\n=== TASK 2 (Cleaned Python Streaming) ===")
print("Total Unique Words  :", len(t2))
print("Total Word Occurrences:", sum(c for _, c in t2))
print("\nTop 15 Most Frequent Cleaned Words in Task 2:")
for w, c in t2_sorted[:15]:
    print("  {:<15} : {}".format(w, c))

t1_dict = dict(t1)
t2_dict = dict(t2)

chars = ["ahab", "ishmael", "queequeg", "starbuck"]
themes = ["whale", "sea", "ship", "boat", "harpoon", "captain", "ocean", "water"]

print("\n=== TASK 3 PREVIEW: CHARACTER ANALYSIS ===")
for ch in chars:
    print("  Character: {:<10} | Task 2 Cleaned Count: {}".format(ch, t2_dict.get(ch, 0)))

print("\n=== TASK 3 PREVIEW: THEMATIC KEYWORDS ===")
for th in themes:
    print("  Theme: {:<10} | Task 2 Cleaned Count: {}".format(th, t2_dict.get(th, 0)))

# Automatically export both datasets to CSV files in the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
csv1_path = os.path.join(script_dir, "task1_result.csv")
csv2_path = os.path.join(script_dir, "task2_result.csv")

print("\n=== EXPORTING CSV FILES ===")
export_to_csv(t1, csv1_path)
export_to_csv(t2, csv2_path)
print("Done! Both CSV files have been generated.")
