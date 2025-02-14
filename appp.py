import streamlit as st
import pandas as pd

class Questionnaire:
    def __init__(self):
        self.score = 0
        self.responses = {}
    
    def ask_question(self, question, options, max_points):
        """Ask a question with multiple-choice options and ensure balanced scoring."""
        selected_option = st.radio(question, list(options.keys()), key=question)
        self.score += (options[selected_option] / max(options.values())) * max_points
        self.responses[question] = selected_option
    
    def follow_up(self, condition, follow_up_question):
        """Display follow-up questions based on previous responses."""
        if condition in self.responses.values():
            self.responses[follow_up_question] = st.text_input(follow_up_question, key=follow_up_question)
    
    def calculate_score(self):
        """Ensure the final score is capped at 100."""
        self.score = min(self.score, 100)

    def run(self):
        st.title("🎮 Game Feasibility Questionnaire")
        st.write("Evaluate your game concept based on market demand, development feasibility, and strategy.")

        with st.form("questionnaire_form"):
            st.subheader("📌 Basic Questions (Each contributing equally)")
            
            # Game Genre Question (16 points)
            self.ask_question("What is the genre of the game compared to previous projects?", 
                              {"Same": 10, "Different": 5, "Slightly different": 7}, max_points=16)
            self.follow_up("Different", "Why is this genre change beneficial?")

            # Team Capability Question (16 points)
            self.ask_question("How well-equipped is your team to develop this game?", 
                              {"Perfect": 10, "Average": 5, "Low": 2}, max_points=16)
            self.follow_up("Low", "What measures will you take to improve capability?")

            # Level Progression Question (16 points)
            self.ask_question("What type of level progression does the game have?", 
                              {"Linear": 7, "Multi-path": 10}, max_points=16)
            self.follow_up("Multi-path", "How does this enhance the gameplay experience?")

            # Market Demand & Supply Question (16 points)
            self.ask_question("How does demand compare to supply in the market?", 
                              {"Demand = Supply": 7, "Demand > Supply": 10, "Demand < Supply": 5}, max_points=16)
            self.follow_up("Demand < Supply", "What strategies will be used to increase demand?")

            # Market Research Section (Single Question with Weighted Score - 16 points)
            st.subheader("📊 Market Research (Weighted as a single question)")
            market_research_score = 0
            trend_analysis = st.radio("Did you conduct trend analysis?", ["Yes", "No"], key="trend_analysis")
            
            if trend_analysis == "Yes":
                ref_game = st.radio("Do they have a reference game on mobile?", ["Yes", "No"], key="ref_game")
                if ref_game == "Yes":
                    st.text_input("Attach the reference game link:", key="ref_game_link")
                    market_research_score += 5  # Adjusted scoring

                family_size = st.number_input("What is the family size?", min_value=1, step=1, key="family_size")
                market_research_score += 5 if 3 <= family_size <= 5 else 3 if 6 <= family_size <= 10 else 2

                st.text_input("Enter total family downloads:", key="family_downloads")
                st.text_input("Enter last 30 days downloads of the family:", key="family_30days")
                st.text_input("Enter per day installs of the family:", key="family_per_day")

                st.text_input("Enter total downloads of the biggest game:", key="biggest_game")
                st.text_input("Enter last 30 days downloads of the biggest game:", key="biggest_30days")
                st.text_input("Enter per day installs of the biggest game:", key="biggest_per_day")

                st.text_input("Enter total downloads of the top growing game:", key="top_growing_game")
                st.text_input("Enter last 30 days downloads of the top growing game:", key="top_growing_30days")
                st.text_input("Enter per day installs of the top growing game:", key="top_growing_per_day")

                chart_trend = st.radio("Does the all-time download chart of the family show gradual growth or decline?", 
                                       ["Growth", "Stable", "Decline"], key="chart_trend")
                market_research_score += {"Growth": 5, "Stable": 3, "Decline": 1}[chart_trend]

            # Normalize market research score to fit 16-point range
            self.score += (market_research_score / 15) * 16  # Scaling to max 16 points

            # Development Approach (16 points)
            st.subheader("🛠 Development Strategy")
            self.ask_question("Which development approach is being used?", 
                              {"Copy Cat": 5, "Pattern Copy": 7, "Theme Different": 10, "80/20": 8, "70/30": 7, "50/50 Merge": 6}, max_points=16)
            self.follow_up("Copy Cat", "What differentiates your game from competitors?")

            self.ask_question("Is the theme relevant?", 
                              {"Relevant to core gameplay": 7, "Targets broader audience": 7, "Both": 10}, max_points=16)
            self.follow_up("Both", "How does the theme balance core gameplay and mass appeal?")

            # Submit button
            submitted = st.form_submit_button("Submit & Calculate Score")
        
        if submitted:
            self.calculate_score()
            
            st.subheader("🔢 Final Score:")
            st.progress(self.score / 100)
            st.write(f"**Your Game Feasibility Score: {round(self.score, 2)} / 100**")
            
            # Outcome Messages
            if self.score > 80:
                st.success("🚀 Your game will go to the moon! 🎉")
            elif 50 <= self.score <= 80:
                st.warning("⚠️ Risk factor alert! Consider improving feasibility.")
            else:
                st.error("💀 Your game will join the graveyard even before you!")

            # Save responses
            response_data = self.responses
            response_data["Score"] = round(self.score, 2)
            df = pd.DataFrame([response_data])
            st.download_button("Download Responses as CSV", df.to_csv(index=False), "game_feasibility.csv", "text/csv")

if __name__ == "__main__":
    q = Questionnaire()
    q.run()
