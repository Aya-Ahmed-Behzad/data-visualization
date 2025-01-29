import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1- Importing data
df = pd.read_csv('medical_examination.csv')

# 2- Adding the 'overweight' column
df['overweight'] = (df['weight'] / (df['height'] / 100) ** 2) > 25
df['overweight'] = df['overweight'].astype(int)

# 3- Normalization (0: good, 1: bad)
df['cholesterol'] = df['cholesterol'].map({1: 0, 2: 1, 3: 1})
df['gluc'] = df['gluc'].map({1: 0, 2: 1, 3: 1})

# 4- Categorical Plot
def draw_cat_plot():
    # Melting the dataframe for easy plotting
    df_cat = pd.melt(df, id_vars=['cardio'],
                     value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'],
                     var_name='variable', value_name='value')

    # Grouping by 'cardio', 'variable', 'value' and counting occurrences
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')

    # Create graph for the categorical plot (bar plot)
    g = sns.catplot(
        data=df_cat,
        x="variable",           # Categorical variable for x-axis
        y="total",              # Numeric variable for y-axis (count of occurrences)
        hue="value",            # Grouping variable
        kind="bar",             # Bar plot
        col="cardio",           # Facet by 'cardio' column
        height=4,               # Height of each facet
        aspect=1.3              # Aspect ratio of the plot
    )

    g.set_axis_labels("variable", "total")
    g.set_titles(col_template="Cardio = {col_name}")
    g.add_legend(title='Value')

    # Save the plot as an image
    fig= g
    fig.savefig('catplot.png')
    
    return fig

# 5- Heatmap Plot
def draw_heat_map():
    # Cleaning the data by applying several conditions
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) &
                 (df['weight'] >= df['weight'].quantile(0.025)) &
                 (df['height'] <= df['height'].quantile(0.975)) &
                 (df['height'] >= df['height'].quantile(0.025)) &
                 (df['weight'] <= df['weight'].quantile(0.975))]

    # Calculating the correlation matrix
    corr = df_heat.corr()

    # Masking the upper triangle of the correlation matrix
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Creating the heatmap plot
    fig, ax = plt.subplots(figsize=(12, 12))
    
    sns.heatmap(corr,
    vmin=-0.099,
    vmax=0.28,
    center= 0.01,
    annot=True,
    fmt='.1f',
    linewidths=0.5,
    linecolor='white',
    cbar=True,
    cbar_kws= {'shrink': .4},
    square=True,
    mask=mask,
    ax=ax)
    # Save the heatmap as an image
    fig.savefig('heatmap.png')

    return fig
