import streamlit as st
import requests
import plotly.graph_objects as go

# this is the main function in which we define our webpage  
def main():
    st.markdown("# Wine Quality Prediction App 🍷🍇")
    st.markdown("### This app is meant to predict red wine quality " +
            "according to different chemical")

    # slider version 
    volatile_acidity = st.slider('Volatile Acidity', 0.0, 2.0, 0.319, 0.001) 
    alcohol = st.slider('Alcohol', 0.0, 16.0, 11.634, 0.01) 

    st.text(volatile_acidity)
    st.text(alcohol)

    # Bouton pour prédire la qualité
    if st.button('Prédire la qualité du vin', type='primary'):
        # Appel à l'API
        api_url = "https://jgwineapi-dbfsbyhyg9hrg0c5.francecentral-01.azurewebsites.net/predict"
        data = {
            "alcohol": alcohol,
            "volatile_acidity": volatile_acidity
        }
        
        try:
            response = requests.post(api_url, json=data)
            response.raise_for_status()
            
            # Récupération de la probabilité
            result = response.json()
            
            # Extraire la prédiction et la probabilité
            prediction = result.get('prediction', 0)
            probability_list = result.get('probability', [0, 0])
            
            # La première valeur de probability indique la probabilité de la prédiction
            probability = probability_list[1] if isinstance(probability_list, list) and len(probability_list) > 0 else 0
            
            # Affichage du KPI
            st.markdown("---")
            st.markdown("### 📊 Résultat de la prédiction")
            
            # Affichage de la probabilité comme un KPI
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.metric(
                    label="Probabilité que le vin soit bon" if prediction == 1 else "Probabilité que le vin ne soit pas bon",
                    value=f"{probability * 100:.2f}%",
                    delta=None
                )
                
                # Indicateur visuel supplémentaire
                if prediction == 1:
                    if probability >= 0.7:
                        st.success("🍷 Excellente qualité probable!")
                    elif probability >= 0.5:
                        st.info("👍 Bonne qualité probable")
                    else:
                        st.warning("⚠️ Qualité probable mais avec incertitude")
                else:
                    st.error("❌ Qualité insuffisante probable")
            
            # Graphique Plotly - Jauge de probabilité
            st.markdown("### 📈 Visualisation")
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = probability * 100,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Confiance de la prédiction", 'font': {'size': 24}},
                number = {'suffix': "%", 'font': {'size': 40}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkgray"},
                    'bar': {'color': "darkblue"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 50], 'color': '#ffcccc'},
                        {'range': [50, 70], 'color': '#fff3cd'},
                        {'range': [70, 100], 'color': '#d4edda'}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 50
                    }
                }
            ))
            
            fig.update_layout(
                height=350,
                margin=dict(l=20, r=20, t=50, b=20),
                paper_bgcolor="white",
                font={'color': "darkblue", 'family': "Arial"}
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Graphique en barres comparant les deux probabilités
            st.markdown("### 📊 Détail des probabilités")
            
            fig2 = go.Figure(data=[
                go.Bar(
                    x=['Mauvaise qualité', 'Bonne qualité'],
                    y=[probability_list[0] * 100, probability_list[1] * 100],
                    text=[f"{probability_list[0]*100:.2f}%", f"{probability_list[1]*100:.2f}%"],
                    textposition='auto',
                    marker_color=['#ff6b6b', '#51cf66']
                )
            ])
            
            fig2.update_layout(
                title="Probabilités pour chaque classe",
                yaxis_title="Probabilité (%)",
                xaxis_title="Catégorie",
                height=400,
                showlegend=False,
                paper_bgcolor="white",
                plot_bgcolor="white"
            )
            
            st.plotly_chart(fig2, use_container_width=True)
                    
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Erreur lors de l'appel à l'API: {str(e)}")
        except Exception as e:
            st.error(f"❌ Erreur inattendue: {str(e)}")

# Init code
if __name__=='__main__': 
    main()
