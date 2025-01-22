import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
     page_title="Análise: Previsão de Renda",
     page_icon="https://empreenderdinheiro.com.br/wp-content/uploads/2019/07/economia.jpeg",
     layout="wide",
)

st.write('# Análise exploratória: Previsão de renda')
 
# Carregando banco de dados
renda_raw = pd.read_csv('./input/previsao_de_renda.csv')
# Tratamento básico dos dados
renda1 = renda_raw.drop(['Unnamed: 0', 'id_cliente'], axis=1)
renda = renda1.dropna()

# Adicionando filtro para determinado período
renda.data_ref = pd.to_datetime(renda.data_ref) # Coluna para o formato de datas
# Definindo os máximos e mínimos 
min_data = renda.data_ref.min()
max_data = renda.data_ref.max()

# Ordenando
datas = pd.DataFrame(renda.data_ref.unique(), columns=['data_ref'])
datas.sort_values(by='data_ref', inplace=True, ignore_index=True)
# st.write(datas)
# Definindo uma barra lateral com o período de interesse
st.sidebar.markdown("# <h1 style='text-align: center; color: purple;'>Selecione o período de interesse</h1>", 
                    unsafe_allow_html=True)

data_inicial = st.sidebar.date_input('Selecione a data inicial:', 
                                     value = min_data,
                                     min_value = min_data, 
                                     max_value = max_data)
data_final = st.sidebar.date_input('Selecione a data final:',
                                    value = max_data, 
                                    min_value = min_data,
                                    max_value = max_data)
st.sidebar.markdown('-------------')
# Seleção de datas
st.sidebar.write('Intervalo de datas disponível:')
st.sidebar.write('Inicial -', min_data)
st.sidebar.write('Final -', max_data)

# Definindo os limitadores a partir das datas definidas
df_renda = renda[(renda['data_ref'] <= pd.to_datetime(data_final)) 
                & (renda['data_ref'] >= pd.to_datetime(data_inicial))]

# Gerando colunas
left_column, right_column = st.columns(2) # Cria o número de colunas especificado

with left_column:
     st.markdown('#### Dicionário de dados:')
     if st.checkbox('Exibir dicionário!'): # Para exibir a tabela de metadados
          st.markdown('''
                    | Variável                | Descrição                                           | Tipo         |
                    | ----------------------- |:---------------------------------------------------:| ------------:|
                    | data_ref                |  Data de registro das informações                   | string|
                    | id_cliente              |  Identificador exclusivo do cliente                 | int |
                    | sexo                    |  F = 'Feminino'; M = 'Masculino'                    | string |
                    | posse_de_veiculo        |  False = "Não possui"; "True = Possui"              | bool | 
                    | posse_de_imovel         |  False = "Não possui"; "True = Possui"              | bool |
                    | qtd_filhos              |  Quantidade de filhos                               | int |
                    | tipo_renda              |  Tipo de renda (ex: Empresário, Assalariado etc.)   | string |
                    | educacao                |  Grau de escolaridade (ex: Primário, Secundário etc.)| string |
                    | estado_civil            |  Estado civil (ex: Solteiro, Casado etc.)           | string |
                    | tipo_residencia         |  Tipo de residência (ex: Casa, Aluguel etc.)        | string |
                    | idade                   |  Idade do cliente (em anos)                         | int |
                    | tempo_emprego           |  Tempo de emprego (em anos)                         | float |
                    | qt_pessoas_residencia   |  Número de pessoas na residência                    | float |
                    | renda                   |  Valor da renda mensal                              | float |            
                    ''')
          
with right_column: #Utiliza a coluna da esquerda
    st.markdown('#### Dataframe utilizado:')
    if st.checkbox('Exibir DataFrame!'): #Exibe o dataframe quando o checkbox é selecionado
        st.write('- Shape do DataFrame:', df_renda.shape)
        st.write('- Período selecionado: ', data_inicial,'--', data_final)
        df_renda  #Exibe o dataframe 


st.write('## Análise univariada')
st.write('- ##### Gráficos de contagem das variáveis em relação a seus respectivos componentes:')
with st.container():
     col1, col2, col3 = st.columns(3)
     with col1:
          # st.subheader('Escolaridade')
          # plt.figure(figsize=[.5, .5])
          fig1 = px.pie(df_renda, names='educacao', title='Escolaridade')
          st.plotly_chart(fig1)
          
          # st.subheader('Contagem por sexo')
          fig2 = px.histogram(df_renda, x='sexo', title='Sexo')
          st.plotly_chart(fig2)

          fig3 = px.histogram(df_renda, x='qtd_filhos', title='Quantidade de filhos')
          st.plotly_chart(fig3)
     
     with col2:
          # st.subheader('Tipo de renda')
          fig1 = px.histogram(df_renda, x='tipo_renda', title='Tipo de renda')
          st.plotly_chart(fig1)

          # st.subheader('Estado civil')
          fig2 = px.pie(df_renda, names='estado_civil', title='Estado civil')
          st.plotly_chart(fig2)

          fig3 = px.histogram(df_renda, x='qt_pessoas_residencia', title='Quantidade de pessoas na residência')
          st.plotly_chart(fig3)

     with col3:
          # st.subheader('Posse de imóvel')
          fig1 = px.histogram(df_renda, x='posse_de_imovel', title='Posse de imóvel')
          st.plotly_chart(fig1)

          # st.subheader('Posse de veículo')
          fig2 = px.histogram(df_renda, x='posse_de_veiculo', title='Posse de veiculo')
          st.plotly_chart(fig2)

          fig3 = px.pie(df_renda, names='tipo_residencia', title='Tipo de residência')
          st.plotly_chart(fig3)          

          

with st.container():
     col1, col2 = st.columns(2)

     with col1:
          # st.subheader('Tempo de emprego')
          fig = px.histogram(df_renda, x='tempo_emprego', nbins=15, title='Tempo de emprego',
                             marginal='box', opacity=1)
          st.plotly_chart(fig)

     with col2:
          # st.subheader('Idade')
          fig = px.histogram(df_renda, x='idade', nbins=25, title='Idade',
                             marginal='box')
          st.plotly_chart(fig)
     


st.write('## Análise bivariada')


fig = px.histogram(df_renda, x='data_ref', color='tipo_renda', barmode='group',
                   title='Contagem da variável "tipo_renda" em relação à "data_ref"',
               #     marginal='box' 
                   )
st.plotly_chart(fig)


fig = px.histogram(df_renda, x='data_ref', color='educacao', barmode='group',
                   title='Contagem da variável "educacao" em relação à "data_ref"')
st.plotly_chart(fig)


var=['sexo', 'posse_de_veiculo', 'posse_de_imovel']
for _ in var:
     fig = px.histogram(df_renda, x=df_renda['data_ref'], y=df_renda['renda'], color=_, barmode='group',
                    histfunc='avg', 
                    title=f'Renda média em função da "data_ref" com relação a variável "{_}".') 
     st.plotly_chart(fig)


# Scatter
fig = px.scatter(df_renda, x='tempo_emprego', y = 'renda', opacity=.7, 
                 marginal_x='box', marginal_y='box', trendline='ols', trendline_color_override='#8A2BE2', 
                 title='Distribuição da renda em relação ao tempo de emprego')
st.plotly_chart(fig)

# Renda em função da escolaridade 
table = pd.pivot_table(data=df_renda, values='renda', index='educacao', aggfunc='mean').reset_index()
# Gerando a figura
fig = px.line(table, x='educacao', y='renda', line_shape='linear', 
              title='Distribuição da renda média em função da escolaridade')
st.plotly_chart(fig)        


# Analisando correlação entre as variáveis numéricas
st.write('#### Analisando a correlação entre as variáveis')
number = df_renda[['tempo_emprego', 'sexo', 'tipo_renda', 'idade', 'educacao', 'estado_civil', 'posse_de_imovel']]
number = pd.get_dummies(number)
# Matriz de correlação 
if st.checkbox('Matriz de correlação'):
     st.write(number.corr())
# Visualização gráfica
fig = px.imshow(number.corr(), text_auto='.2f',
                aspect='auto', width=1300, height=1300,
                title='Correlação entre as variáveis de interesse obtidas pelo "stepwise selection"')
st.plotly_chart(fig)


# Outro formato de plot

# plt.figure(figsize=[25,25])
# fig = sns.heatmap(number.corr(), annot=True, fmt='.2f')
# st.pyplot(plt)