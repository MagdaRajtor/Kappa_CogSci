import pandas as pd
#scikit-learn package
from sklearn.metrics import cohen_kappa_score

def kappa(data, col1, col2):
    with open(data, encoding="utf8") as f:
        file = pd.read_csv(f, sep='\t', header=0)
        ann1 = file[col1].to_list()
        ann2 = file[col2].to_list()
        result = cohen_kappa_score(ann1, ann2)
        return round(result, 4)

def precision(data, col):
    with open(data, encoding="utf8") as f:
        file = pd.read_csv(f, sep='\t', header=0)
        vals = file[col].value_counts()  # count values in column
        discard = vals["?"] if "?" in vals else 0  # number of '?' decisions to remove
        accurate = vals["Y"] if "Y" in vals else 0  # number of 'Y' decisions
        nans = file[col].isna().sum()  # number of rows without value
        if accurate != 0:
            return round((file.shape[0] - discard - nans) / accurate, 3)
        else:
            return "Nie można obliczyć precision. Liczba wierszy z wynikiem 'Y' wynosi zero"

print("Plik 'Sample Accuracy All Annotators'")
print("kappa: ", kappa("data/Sample Accuracy All Annotators - Data.tsv", "evaluation 1", "evaluation 2"))
print("precision: ", precision("data/Sample Accuracy All Annotators - Data.tsv", "superannotator"))
print("----------------")
print("Plik 'Sample_accuracy_recall_superannotator'")
print("kappa: ", kappa("data/Sample_accuracy_recall_superannotator - Data.tsv", "Normalized Ann1", "Normalized Ann2"))
#tylko zobaczyć funkcja czy działa:
#print("precision: ", precision("data/Sample_accuracy_recall_superannotator - Data.tsv", "Decision"))