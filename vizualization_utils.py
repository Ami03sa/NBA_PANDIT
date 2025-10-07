import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict, List, Any
import json

class VisualizationRenderer:
    """Renders visualizations from structured data"""
    
    @staticmethod
    def render_table(data: List[Dict], title: str = "NBA Statistics") -> str:
        """
        Render data as a formatted markdown table
        """
        if not data:
            return "No data available"
        
        df = pd.DataFrame(data)
        table = df.to_markdown(index=False)
        return f"### {title}\n\n{table}"
    
    @staticmethod
    def render_bar_chart(data: List[Dict], x_key: str, y_key: str, 
                        title: str, xlabel: str, ylabel: str,
                        save_path: str = None):
        """
        Create a bar chart comparing values
        """
        df = pd.DataFrame(data)
        
        plt.figure(figsize=(10, 6))
        plt.bar(df[x_key], df[y_key], color='#1d428a')  # NBA blue
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    @staticmethod
    def render_line_chart(data: List[Dict], x_key: str, y_keys: List[str],
                         title: str, xlabel: str, ylabel: str,
                         save_path: str = None):
        """
        Create a line chart for trends over time
        """
        df = pd.DataFrame(data)
        
        plt.figure(figsize=(12, 6))
        for y_key in y_keys:
            plt.plot(df[x_key], df[y_key], marker='o', label=y_key, linewidth=2)
        
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    @staticmethod
    def render_comparison_table(players_data: List[Dict], stat_columns: List[str]) -> str:
        """
        Create a comparison table for multiple players
        """
        df = pd.DataFrame(players_data)
        
        if stat_columns:
            # Only show specified columns
            columns_to_show = ['Player'] + [col for col in stat_columns if col in df.columns]
            df = df[columns_to_show]
        
        table = df.to_markdown(index=False)
        return f"### Player Comparison\n\n{table}"
    
    @staticmethod
    def create_viz_from_agent_output(viz_data: str):
        """
        Parse visualization agent output and render accordingly
        """
        try:
            # Try to parse as JSON
            viz_config = json.loads(viz_data)
            
            viz_type = viz_config.get('visualization_type')
            title = viz_config.get('title', 'NBA Statistics')
            data = viz_config.get('data', [])
            config = viz_config.get('config', {})
            
            if viz_type == 'table':
                return VisualizationRenderer.render_table(data, title)
            elif viz_type == 'bar_chart':
                VisualizationRenderer.render_bar_chart(
                    data,
                    config.get('x_key', 'name'),
                    config.get('y_key', 'value'),
                    title,
                    config.get('xlabel', 'X'),
                    config.get('ylabel', 'Y')
                )
            elif viz_type == 'line_chart':
                VisualizationRenderer.render_line_chart(
                    data,
                    config.get('x_key', 'season'),
                    config.get('y_keys', ['value']),
                    title,
                    config.get('xlabel', 'Season'),
                    config.get('ylabel', 'Value')
                )
        except json.JSONDecodeError:
            # If not JSON, return as is (might be markdown table)
            return viz_data


# Example usage functions
def example_player_comparison():
    """Example: Compare two players"""
    data = [
        {'Player': 'LeBron James', 'PPG': 27.2, 'RPG': 7.5, 'APG': 7.3},
        {'Player': 'Kevin Durant', 'PPG': 27.3, 'RPG': 7.0, 'APG': 4.3}
    ]
    
    print(VisualizationRenderer.render_table(data, "Player Comparison"))
    VisualizationRenderer.render_bar_chart(
        data, 'Player', 'PPG',
        'Points Per Game Comparison',
        'Player', 'PPG'
    )


def example_career_progression():
    """Example: Show career progression"""
    data = [
        {'Season': '2018-19', 'PPG': 27.4},
        {'Season': '2019-20', 'PPG': 25.3},
        {'Season': '2020-21', 'PPG': 25.0},
        {'Season': '2021-22', 'PPG': 30.3},
        {'Season': '2022-23', 'PPG': 28.9},
    ]
    
    VisualizationRenderer.render_line_chart(
        data, 'Season', ['PPG'],
        'LeBron James Career PPG Progression',
        'Season', 'Points Per Game'
    )