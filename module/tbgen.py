# %%
import re as regex

def matrix_to_latex(matrix_text):
    # Remove square brackets and split rows
    matrix_text = matrix_text.replace('[', '').replace(']', '')
    rows = matrix_text.split('\n')
    
    # Format each element based on its value
    formatted_rows = []
    for row in rows:
        formatted_row = " & ".join([
            "0" if float(num) == 0 or abs(float(num)) < 1e-10 else (
                f"{float(num):3.3f}" if 0.01 <= abs(float(num)) < 1000 else f"{float(num):.2e}".replace('e', 'e^{') + '}'
            )
            for num in row.split()
        ])
        formatted_rows.append(formatted_row)
    
    # Join rows with LaTeX matrix syntax, wrapped in dollar signs for math mode
    #latex_matrix = "$\\begin{bmatrix} " + " \\\\ ".join(formatted_rows) + " \\end{bmatrix}$"
    latex_matrix = "\\( \\begin{bmatrix} " + " \\\\ ".join(formatted_rows) + " \\end{bmatrix} \\)"
    return latex_matrix

# Function deletes any repeadted values in a column and gives the index of the last repetition for hlines generation
def multirow_latex(df, table_data, header):
    
    df.reset_index(drop=True, inplace=True) #converts index to be low to high 
    multirow_count = 0 #counts how many rows are repeated
    hlines = f"hline{{" #initilizes where the hline will be placed
    
    # Loops through entire row of df and checks any repetitions
    prev_val = df[header][0] #initilializes the first value
    for index in range(1, len(table_data.index)):

        #checks if next value has the same  value
        if df[header][index] == prev_val:
            
            multirow_count += 1

            if multirow_count == 1:
                index_first = index
                value_frist = df[header][index]
                df.loc[index, header] = ''
                
            else:
                df.loc[index, header] = ''

        else:

            if multirow_count == 0:
                hlines = hlines + f"{index+2},"

            if multirow_count >= 1:
                df.loc[index_first-1, header] = f"\\SetCell[r={multirow_count+1}]{{m}} {{{value_frist}}}"
                #hlines = hlines + f"{index_first+1},"
                hlines = hlines + f"{index+2},"

            multirow_count = 0
            prev_val = df[header][index]
    
    hlines = hlines[::-1].replace(",", "", 1)[::-1]
    hlines = hlines + f"}} = {{1pt}}"
    return df, hlines

def unique_hline(hline_base, hline_sub):

    # Extract the numbers from each string using regex
    num_base = set(map(int, regex.findall(r'\d+', hline_base)))
    num_sub = set(map(int, regex.findall(r'\d+', hline_sub)))

    # Find the unique numbers in hline2 that are not in hline1
    unique_numbers = sorted(num_sub - num_base)

    # Reformat the strings
    new_hline_base = f"hline{{{','.join(map(str, sorted(num_base)))}}} = {{1pt}}"
    new_hline_sub = f"hline{{{','.join(map(str, unique_numbers))}}} = {{1pt}}"

    return new_hline_sub