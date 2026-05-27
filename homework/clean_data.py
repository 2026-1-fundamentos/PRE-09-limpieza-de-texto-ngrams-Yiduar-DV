"""Taller evaluable presencial"""

import string

import pandas as pd  # type: ignore

def create_key(df, n):
    """Cree una nueva columna en el DataFrame que contenga el key de la
    columna 'text'"""

    df = df.copy()
    df["key"] = df["raw_text"]
    df["key"] = df["key"].str.strip()
    df["key"] = df["key"].str.lower()
    df["key"] = df["key"].str.replace("-", "")
    df["key"] = df["key"].str.translate(
        str.maketrans("", "", string.punctuation+" ")
    )

    # ------------------------------------------------------
    # Esta es la parte especifica del algoritmo de n-gram:
    #
    # - Convierta el texto a una lista de n-gramas
    df["key"] = df["key"].map(
        lambda x: [x[t : t + n] for t in range(len(x))],
    )
    #
    # - Ordene la lista de n-gramas y remueve duplicados
    df["key"] = df["key"].apply(lambda x: sorted(set(x)))
    #
    # - Convierta la lista de ngramas a una cadena
    df["key"] = df["key"].str.join("")
    # ------------------------------------------------------

    return df


def generate_cleaned_column(df):
    """Crea la columna 'cleaned' en el DataFrame"""

    #
    # Este código es identico al anteior
    #
    keys = df.copy()
    keys = keys.sort_values(by=["key", "raw_text"], ascending=[True, True])
    keys = keys.drop_duplicates(subset="key", keep="first")
    key_dict = dict(zip(keys["key"], keys["raw_text"]))
    df["cleaned_text"] = df["key"].map(key_dict)

    return df


def main(input_file, output_file, n=2):
    """Ejecuta la limpieza de datos"""
    #
    # Este código es identico al anteior
    #
    df = pd.read_csv(input_file)
    df = create_key(df, n)
    df = generate_cleaned_column(df)
    df.to_csv("files/test.csv", index=False)
    df[["raw_text", "cleaned_text"]].to_csv(output_file, index=False)


if __name__ == "__main__":
    main(
        input_file="files/input.txt",
        output_file="files/output.txt",
    )