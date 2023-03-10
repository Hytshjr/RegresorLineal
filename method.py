import pandas as pd
import matplotlib as plt
import seaborn as sns
import pipe

@pd.api.extensions.register_dataframe_accessor('missing')

class InfoMissingAll:

    def __init__(self, null_obj):

        self._null = null_obj # Declaramos el objeto principal que es el DataFrame

    def missing_info(self):

    # Informa sobre todos los valores nulls que hay en el DataFrame
    
        try:
            dataframe = self._null.isna().sum().sort_values(ascending = False).reset_index()
            return dataframe.assign(Datos=self._null.shape[0])
        except NameError as _e:
            print(_e)

    def missing_graf(self):
    
    #Crea una grafica en porcentaje en que estan ditribuidos los nulls por una variable
    
        try:
            (
                self._null
                .isna()
                .melt()
                .pipe(
                    lambda df: (
                        sns.displot(
                            data = df,
                            y = 'variable',
                            hue = 'value',
                            multiple = 'fill',
                            aspect = 3,
                            bins = 1
                        )
                    )
                )
            )
        
        except NameError as _e:
            print(_e)
    
    def missing_id(self, graf,num):
        try:
            nulos_fil = {}
            list_id = []
            nulls_np = []

            for i in range(self._null.shape[0]):            
                df = self._null.iloc[i]
                nulls = 0

                for x in range(self._null.shape[1]):
                    if self._null.iloc[i].isnull().iloc[x] == True:
                        nulls +=1

                if nulls > 0:                
                    list_id.append(df.iloc[0])
                    nulls_np.append(nulls)

            nulos_fil['Id'] = list_id
            nulos_fil['Nulls'] = nulls_np
                    
            df = pd.DataFrame(nulos_fil)

            if graf == True:
                return df
            
            else:
                df_min = df[df['Nulls']>num]
                (
                    df_min.sort_values(by='Nulls',ascending=True)
                    .pipe(
                        lambda df: (
                            sns.catplot(
                                data = df,
                                y = 'Id',
                                x = 'Nulls',
                                hue = 'Nulls',
                                kind="bar",
                                aspect=2.5,
                                height=df.shape[0]//3
                            )
                        
                        )
                    )
                )
        except NameError as _e:
            print(_e)

    def duplicate_id(self,index):
            
        try:
            lista_id = []
            lista_id_com = []
            index_iloc = []
            duplicate = {}

            for i in range(self._null.shape[0]):            
                df = self._null.iloc[i]
                df_id = df.iloc[index]
                
                for x in range(self._null.shape[0]):

                    if i != x:
                        df_com = self._null.iloc[x]
                        id_com = df_com.iloc[index]
                        
                        if df_id == id_com:
                            lista_id.append(df_id)
                            lista_id_com.append(id_com)
                            index_iloc.append(i)

            duplicate['Index'] = lista_id
            duplicate['Index_duplicado'] = lista_id_com
            duplicate['Index_iloc'] = index_iloc

            return pd.DataFrame(duplicate)
        
        except NameError as _e:
            print(_e)

@pd.api.extensions.register_dataframe_accessor('grafic')

class GrafigCatNp:
    def __init__(self,frame_grafic):
      
        self._frame =  frame_grafic
    
    def grafic_number(self,nfil,ncolum):
        colum = self._frame.select_dtypes(include = ['float64', 'int']).columns
        fig, axes = plt.pyplot.subplots(nrows= nfil, ncols=ncolum, figsize=(len(colum)*2.5,len(colum)*2), dpi=200)

        axes = axes.flat

        for i, col in enumerate(colum):
            sns.distplot(
            self._frame[col],
            color   = "blue",
            rug     = True,
            kde_kws = {'fill': True, 'linewidth': 1},
            hist=False,
            ax=axes[i]
            )

            axes[i].set_title(col, fontsize = 'medium')
            axes[i].tick_params(labelsize = 6)
    
    def grafic_cat(self,nfil,ncolum):
        colum = self._frame.select_dtypes(include = ['object']).columns
        fig, axes = plt.pyplot.subplots(nrows= nfil, ncols=ncolum, figsize=(len(colum)*2.5,len(colum)*2), dpi=200)

        axes = axes.flat

        for i, col in enumerate(colum):
            sns.histplot(
            self._frame[col],
            ax=axes[i]
            )

            axes[i].set_title(col, fontsize = 'medium')
            axes[i].tick_params(labelsize = 6)