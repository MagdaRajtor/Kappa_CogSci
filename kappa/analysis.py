import csv
import pandas as pd
#scikit-learn package
from sklearn.metrics import cohen_kappa_score

def cohen_kappa(ann1, ann2):
    """Computes Cohen kappa for pair-wise annotators.
    :param ann1: annotations provided by first annotator
    :type ann1: list
    :param ann2: annotations provided by second annotator
    :type ann2: list
    :rtype: float
    :return: Cohen kappa statistic
    """

    count = 0
    for an1, an2 in zip(ann1, ann2):
        if an1 == an2:
            count += 1
    A = count / len(ann1)  # observed agreement A (Po)
    uniq = set(ann1 + ann2)
    print(uniq)
    E = 0  # expected agreement E (Pe)
    for item in uniq:
        cnt1 = ann1.count(item)
        cnt2 = ann2.count(item)
        count = ((cnt1 / len(ann1)) * (cnt2 / len(ann2)))
        E += count
    return round((A - E) / (1 - E), 4)


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
        result = cohen_kappa(ann1, ann2) #ta funkcja bierze pod uwagę wartości nan
        #result = cohen_kappa_score(ann1, ann2)
        return round(result, 4)


def precision(data, col, decision):
    #decision: jakie decyzje liczyć jako trafne - "Y" czy "NA"
    with open(data, encoding="utf8") as f:
        file = pd.read_csv(f, sep='\t', header=0, quoting=csv.QUOTE_NONE)
        #normalizacja wyników w tej kolumnie (zwłaszcza dla drugiego pliku)
        for x in file[col]:
            file[col].replace({x: str(x).upper().strip()}, inplace=True)
        vals = file[col].value_counts()  # count values in column
        check_v(vals)
        discard = vals["?"] if "?" in vals else 0  # number of '?' decisions to remove
        accurate = 0
        if decision == "NA":
            accurate = vals["NAN"] if "NAN" in vals else 0  # number of NaN decisions
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