
import streamlit as st

class Questionnaire:
    def __init__(self):
        self.score = 0
        self.responses = {}
    
    def ask_question(self, question, options):
        selected_option = st.radio(question, list(options.keys()))
        self.score += options[selected_option]
        self.responses[question] = selected_option
    
    def follow_up(self, condition, follow_up_question):
        if condition in self.responses.values():
            st.text_input(follow_up_question)
    
    def run(self):
        st.title("Game Feasibility Questionnaire")
        st.write("Answer the following questions to evaluate your game proposal.")

        self.ask_question("What is the genre of the game compared to previous projects?", 
                          {"Same": 10, "Different": 5, "Slightly different": 7})
        
        self.follow_up("Different", "Why is this genre change beneficial?")
        
        self.ask_question("How well-equipped is your team to develop this game?", 
                          {"Perfect": 10, "Average": 5, "Low": 2})
        
        self.follow_up("Low", "What measures will you take to improve capability?")
        
        self.ask_question("What type of level progression does the game have?", 
                          {"Linear": 7, "Multi-path": 10})
        
        self.follow_up("Multi-path", "How does this enhance the gameplay experience?")
        
        self.ask_question("How does demand compare to supply in the market?", 
                          {"Demand = Supply": 7, "Demand > Supply": 10, "Demand < Supply": 5})
        
        self.follow_up("Demand < Supply", "What strategies will be used to increase demand?")
        
        trend_analysis = st.radio("Did you conduct trend analysis?", ["Yes", "No"])
        if trend_analysis == "Yes":
            ref_game = st.radio("Do they have a reference game on mobile?", ["Yes", "No"])
            if ref_game == "Yes":
                st.text_input("Attach the reference game link:")
                self.score += 10
            else:
                self.score += 0
            
            family_size = st.number_input("What is the family size?", min_value=1, step=1)
            if 3 <= family_size <= 5:
                self.score += 10
            elif 6 <= family_size <= 10:
                self.score += 7
            else:
                self.score += 5
            
            st.text_input("Enter total family downloads:")
            st.text_input("Enter last 30 days downloads of the family:")
            st.text_input("Enter per day installs of the family:")
            
            st.text_input("Enter total downloads of the biggest game:")
            st.text_input("Enter last 30 days downloads of the biggest game:")
            st.text_input("Enter per day installs of the biggest game:")
            
            st.text_input("Enter total downloads of the top growing game:")
            st.text_input("Enter last 30 days downloads of the top growing game:")
            st.text_input("Enter per day installs of the top growing game:")
            
            chart_trend = st.radio("Does the all-time download chart of the family show gradual growth or decline?", ["Growth", "Stable", "Decline"])
            if chart_trend == "Growth":
                self.score += 10
            elif chart_trend == "Stable":
                self.score += 7
            else:
                self.score += 3
        
        self.ask_question("Which development approach is being used?", 
                          {"Copy Cat": 5, "Pattern Copy": 7, "Theme Different": 10, "80/20": 8, "70/30": 7, "50/50 Merge": 6})
        
        self.follow_up("Copy Cat", "What differentiates your game from competitors?")
        
        self.ask_question("Is the theme relevant?", 
                          {"Relevant to core gameplay": 7, "Targets broader audience": 7, "Both": 10})
        
        self.follow_up("Both", "How does the theme balance core gameplay and mass appeal?")
        
        st.write("List up to four similar games:")
        for i in range(1, 5):
            game = st.text_input(f"Game {i}:")
            if game:
                self.score += 5
        
        st.subheader("Final Score:")
        st.write(self.score)
        
        if self.score >= 70:
            st.success("Strong feasibility")
        elif 50 <= self.score < 70:
            st.warning("Moderate feasibility, requires improvements")
        else:
            st.error("High risk, major adjustments needed")

if __name__ == "__main__":
    q = Questionnaire()
    q.run()
