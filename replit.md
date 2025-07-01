# NeuralSprint - AI-Powered Scrum Master Automation

## Overview

NeuralSprint is a cyberpunk-themed AI-powered Scrum management application built with Streamlit. The system automates traditional Scrum Master tasks using a local Qwen3 4B language model, providing teams with intelligent sprint planning, story estimation, daily standups, and retrospective analysis. The application emphasizes data privacy by running AI processing locally through LM Studio.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit with custom cyberpunk CSS theming
- **UI Components**: Multi-page application with tabbed interfaces
- **Styling**: Custom CSS with cyberpunk aesthetics (neon colors, dark theme, glowing effects)
- **Session Management**: Streamlit session state for maintaining application state
- **Responsive Design**: CSS-based responsive layout for different screen sizes

### Backend Architecture
- **Core Modules**: Modular Python architecture with separated concerns
  - `AIClient`: Handles communication with local AI model
  - `ScrumManager`: Core Scrum methodology implementation
  - `DataStore`: File-based data persistence layer
- **AI Integration**: Local Qwen3 4B model accessed via LM Studio REST API
- **Data Processing**: Pandas for data manipulation and analysis

### Data Storage Solutions
- **Primary Storage**: JSON file-based system for lightweight persistence
- **Data Structure**: Separate JSON files for different entities:
  - `stories.json`: User stories and backlog items
  - `sprints.json`: Sprint information and metadata
  - `activities.json`: Daily standup and activity tracking
  - `team.json`: Team member information
  - `settings.json`: Application configuration
- **File Organization**: Centralized `data/` directory structure
- **Data Integrity**: JSON validation and error handling for file operations

## Key Components

### AI Processing Pipeline
- **Local Model**: Qwen3 4B accessed through LM Studio API
- **Prompt Engineering**: Specialized prompts for different Scrum tasks
- **Task Automation**: Story point estimation, sprint planning, standup summaries, retrospective insights
- **Privacy-First**: No external API calls, all processing remains local

### Scrum Management Core
- **Story Management**: Complete user story lifecycle with status tracking
- **Sprint Planning**: AI-assisted sprint creation and capacity planning
- **Daily Standups**: Team progress tracking and blocker identification
- **Retrospectives**: Sprint analysis with AI-generated insights
- **Analytics**: Velocity tracking, burndown charts, and predictive analytics

### User Interface Modules
- **Sprint Planning** (`pages/sprint_planning.py`): Sprint creation and story selection
- **Backlog Management** (`pages/backlog_management.py`): Product backlog organization
- **Daily Standup** (`pages/daily_standup.py`): Daily progress tracking
- **Retrospective** (`pages/retrospective.py`): Sprint analysis and improvement planning
- **Analytics** (`pages/analytics.py`): Performance metrics and insights

## Data Flow

### Story Lifecycle
1. Story creation in backlog management interface
2. AI-powered story point estimation using specialized prompts
3. Sprint assignment during sprint planning
4. Status updates through daily standups
5. Completion tracking and retrospective analysis

### Sprint Management Flow
1. Sprint creation with capacity planning
2. AI-assisted story selection based on team capacity
3. Daily progress monitoring and blocker identification
4. Sprint completion and retrospective generation
5. Historical data analysis for future planning

### AI Processing Pipeline
1. User input captured through Streamlit interface
2. Request formatted and sent to local LM Studio API
3. AI response processed and integrated into application flow
4. Results displayed with cyberpunk-themed UI components

## External Dependencies

### Required Software
- **LM Studio**: Local AI model hosting platform
- **Python 3.8+**: Core runtime environment
- **Streamlit**: Web application framework
- **Plotly**: Interactive data visualization

### AI Model Requirements
- **Model**: Qwen3 4B (or compatible model through LM Studio)
- **Hardware**: RTX 2050+ GPU recommended for optimal performance
- **Memory**: 8GB RAM minimum, 16GB recommended

### Python Dependencies
- Core libraries: `streamlit`, `requests`, `plotly`, `pandas`
- Data handling: `json`, `datetime`, `uuid`
- Visualization: `plotly.graph_objects`, `plotly.express`

## Deployment Strategy

### Local Development
- **Setup**: Clone repository, install dependencies, configure LM Studio
- **Configuration**: Environment variables for LM Studio URL and model selection
- **Data Persistence**: Local file system for development and testing

### Production Considerations
- **Scaling**: Single-user application designed for team-local deployment
- **Data Migration**: JSON files can be easily backed up and transferred
- **Model Updates**: Support for different models through LM Studio configuration
- **Security**: Local-only processing ensures data privacy and security

### Installation Process
1. Install Python 3.8+ and required dependencies
2. Set up LM Studio with Qwen3 4B model
3. Configure environment variables for API endpoints
4. Run Streamlit application locally
5. Access through web browser with cyberpunk interface

## Changelog

```
Changelog:
- June 30, 2025. Initial setup
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```