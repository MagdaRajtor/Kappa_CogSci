import csv
import pandas as pd
#scikit-learn package
from sklearn.metrics import cohen_kappa_score

def check_v(val):
    if len(set(val.values)) > 3:
        print("Uwaga, kolumna", val.name, "zawiera więcej niż 3 wartości:", list(val.index))
        case = input("Czy pokazać ich liczebności? (T/N): ").upper()
        if case == "T":
            print(val)


def kappa(data, col1, col2):
    with open(data, encoding="utf8") as f:
        file = pd.read_csv(f, sep='\t', header=0, quoting=csv.QUOTE_NONE)
        #sprawdzenie wartości
        val1 = file[col1].value_counts()
        val2 = file[col2].value_counts()
        check_v(val1)
        check_v(val2)

        ann1 = file[col1].to_list()
        ann2 = file[col2].to_list()
        result = cohen_kappa_score(ann1, ann2)
        return round(result, 4)


def precision(data, col, decision):
    #decision: jakie decyzje liczyć jako trafne - "Y" czy "NA"
    with open(data, encoding="utf8") as f:
        file = pd.read_csv(f, sep='\t', header=0, quoting=csv.QUOTE_NONE)
        vals = file[col].value_counts()  # count values in column
        check_v(vals)
        discard = vals["?"] if "?" in vals else 0  # number of '?' decisions to remove
        accurate = 0
        if decision == "NA":
            accurate = file[col].isna().sum() # number of NaN decisions
        elif decision == "Y":
            accurate = vals["Y"] if "Y" in vals else 0  # number of 'Y' decisions
        if accurate != 0:
            return round((file.shape[0] - discard) / accurate, 3)
        else:
            return "Nie można obliczyć precision. Liczba wierszy z wynikiem 'Y' wynosi zero"

print("Plik 'Sample Accuracy All Annotators'")
print("kappa: ", kappa("data/Sample Accuracy All Annotators - Data.tsv", "evaluation 1", "evaluation 2"))
print("precision: ", precision("data/Sample Accuracy All Annotators - Data.tsv", "superannotator", "NA"))
print("----------------")
print("Plik 'Sample_accuracy_recall_superannotator'")
print("kappa: ", kappa("data/Sample_accuracy_recall_superannotator - Data.tsv", "Normalized Ann1", "Normalized Ann2"))
#print("precision: ", precision("data/Sample_accuracy_recall_superannotator - Data.tsv", "Decision", "Y"))