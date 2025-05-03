# from langchain_ollama import ChatOllama
# from langgraph.prebuilt import create_react_agent
from langchain_google_community import CalendarToolkit
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import utils, pytz, datetime
from langchain_google_community.calendar.utils import (
    build_resource_service,
    get_google_credentials,
)

class CalendarTool:
    def __init__(self):
        # Can review scopes here https://developers.google.com/gmail/api/auth/scopes
        # For instance, readonly scope is 'https://www.googleapis.com/auth/gmail.readonly'
        # self.credentials = get_google_credentials(
        #     token_file="src/token.json",
        #     scopes=["https://www.googleapis.com/auth/calendar"],
        #     client_secrets_file="src/credentials.json",
        # )
        # creds = None
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
    # Load pre-authorized user credentials from the environment.
        self.path_auth = "src/google_kevin_tieu_tamu_gmail_auth.json"
        # Use OAuth flow to get credentials
        self.flow = InstalledAppFlow.from_client_secrets_file(self.path_auth, self.SCOPES)
        self.credentials = self.flow.run_local_server(port=0)
        # self.api_resource = build_resource_service(credentials=self.creds)
        # self.toolkit = CalendarToolkit(api_resource=self.api_resource)
        self.current_timezone = 'America/Chicago'
    

    # Create a calendar event
    def calender_create_event(self, event_details):
        try:
            service = build('calendar', 'v3', credentials=self.credentials)
            print(event_details)
            event = {
                'summary': event_details['summary'],
                'start': {
                    'dateTime': event_details['start_time'],
                    'timeZone': self.current_timezone,
                },
                'end': {
                    'dateTime': event_details['end_time'],
                    'timeZone': self.current_timezone,
                },
                # 'attendees': [{'email': email} for email in event_details['attendees']],
            }
        except HttpError as error:
            output = f"An error occurred: {error}"
            return output
        # events = calendar_check_conflict(service,event_details)
        # utils.print_level(f"Calendar check status: {events}",VERBAL_LEVEL)
        # if events is not None:
            # output = f"The event {event_details} has conflict with other {events}. Please reschedule."
            # return output

        event = service.events().insert(calendarId='primary', body=event).execute()
        output = f"Event successfully created: {event.get('htmlLink')}"
        return output

    # Check for conflicting events
    def calendar_check_conflict(self,event_details):
        print(event_details)
        service = build('calendar', 'v3', credentials=self.credentials)
        local_tz = pytz.timezone(self.current_timezone)
        start_time = datetime.strptime(event_details['start_time'], "%Y-%m-%dT%H:%M:%S")
        start_time_local = local_tz.localize(start_time).isoformat()
        end_time = datetime.strptime(event_details['end_time'], "%Y-%m-%dT%H:%M:%S")
        end_time_local = local_tz.localize(end_time).isoformat()
        events_result = service.events().list(
            calendarId="primary",
            timeMin=start_time_local,
            timeMax=end_time_local,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        return events
    

    
# calendar_tool = CalendarTool()
# tools = calendar_tool.get_tools()

# llm_model = ChatOllama(model="llama3.2",temperature=0.0, streaming=True)
# agent_executor = create_react_agent(llm_model, tools)

# example_query = "Schedule a meeting with Kevin Tieu on Friday April 25, 2025 Chicago Time at 2 PM for 1 hour. The meeting is about the project update and will be held in the conference room."

# events = agent_executor.stream(
#     {"messages": [("user", example_query)]},
#     stream_mode="values",
# )
# for event in events:
#     event["messages"][-1].pretty_print()