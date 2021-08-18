# Import Libraries
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'IPAexGothic'
import seaborn as sns
import config as cfg 
import pandas as pd

# Parameters
_DATSET_DIR = cfg.dirs["data_dir"]
_OUT_DIR = cfg.dirs["out_dir"]

def vertical_bar_plot(
                    df_dict: dict, 
                    x_label, y_label, title, caption,
                    size=(5,8)):

    plt.figure(figsize=size)
    label_size = 14
    value_size = 14
    g=sns.barplot(x=df_dict.values, y=df_dict.keys())
    for p in g.patches:
            #print(p)
            #print(p.get_y(), p.get_width())
            x = ( df_dict.max() - df_dict.min() )// (df_dict.count()-5)
            y = p.get_y()+0.6
            g.annotate('{:.0f}'.format(p.get_width()), (x, y),
                        ha='left', va='bottom',
                        color= 'black', fontsize=value_size)
    #g.set_xticklabels(unique_col.keys(), fontsize=label_size, fontname='Yu Gothic')
    #for item in g.get_xticklabels(): item.set_rotation(90)
    plt.ylabel(y_label, fontsize=label_size, fontname='Yu Gothic')
    plt.xlabel(x_label, fontsize=label_size, fontname='Yu Gothic')

    plt.title(title, fontsize=label_size, fontname='Yu Gothic')
    #plt.legend()
    plt.tight_layout()
    #degrees = 70
    #plt.xticks(rotation=degrees)
    plt.savefig(f'{_OUT_DIR}/graphs/{caption}.png')
    plt.show()


def two_var_line_plot(
                    df_dict: dict, 
                    x_label, y_label, title, caption,
                    size=(5,8)):

    plt.figure(figsize=(15,5))
    label_size = 14
    value_size = 14
    g=sns.lineplot(x=df_dict.keys(), y=df_dict.values, 
                        #style='label', 
                        marker='o', #dashes=False, 
                         #palette=palette
            )

    #print(g.patches)
    for p in g.patches:
                #print(p)
                plt.annotate('{:.0f}'.format(p.get_height()), (p.get_x()+0.4, p.get_height()),
                                ha='center', va='bottom',
                                color= 'black', fontsize=value_size, fontname='Yu Gothic')
        #g.set_xticklabels(res.keys(), fontsize=label_size, fontname='Yu Gothic')
        #for item in g.get_xticklabels(): item.set_rotation(90)
    plt.xticks(df_dict.keys(), rotation=45)
    plt.ylabel(y_label, fontsize=label_size, fontname='Yu Gothic')
    plt.xlabel(x_label, fontsize=label_size, fontname='Yu Gothic')

    plt.title(title, fontsize=label_size, fontname='Yu Gothic')
    #plt.legend()
    plt.tight_layout()
    #degrees = 70
    #plt.xticks(rotation=degrees)
    plt.savefig(f'{_OUT_DIR}/graphs/{caption}.png')
    plt.show()

def three_var_line_plot(
                df: pd.DataFrame, 
                x: str, y:str, z:str,
                x_label, y_label, title, caption,
                size=(5,8)):

    plt.figure(figsize=(15,5))
    label_size = 14
    value_size = 14
    g=sns.lineplot(x=x, y=y, hue=z, 
                        #style='label', 
                        marker='o', #dashes=False, 
                data=df, #palette=palette
            )

    #print(g.patches)
    for p in g.patches:
                #print(p)
                plt.annotate('{:.0f}'.format(p.get_height()), (p.get_x()+0.4, p.get_height()),
                                ha='center', va='bottom',
                                color= 'black', fontsize=value_size, fontname='Yu Gothic')
        #g.set_xticklabels(res.keys(), fontsize=label_size, fontname='Yu Gothic')
        #for item in g.get_xticklabels(): item.set_rotation(90)
    plt.xticks(df[x].unique(), rotation=45)
    plt.ylabel(y_label, fontsize=label_size, fontname='Yu Gothic')
    plt.xlabel(x_label, fontsize=label_size, fontname='Yu Gothic')

    plt.title(title, fontsize=label_size, fontname='Yu Gothic')
    #plt.legend()
    plt.tight_layout()
    #degrees = 70
    #plt.xticks(rotation=degrees)
    plt.savefig(f'{_OUT_DIR}/graphs/{caption}.png')
    plt.show()
