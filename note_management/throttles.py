from rest_framework.throttling import UserRateThrottle

#Custom throttle class for /notes/upload endpoint (1 request per hour)
class GenerateNotesThrottle(UserRateThrottle):
    scope = 'generate_notes'

#Custom throttle class for /notes/{uuid}/summary endpoint (1 request per 30 minutes)
class GenerateNotesSummaryThrottle(UserRateThrottle):
    scope = 'generate_notes_summary'

#Custom throttle class for /notes/{uuid}/chat ()
class ChatbotThrottle(UserRateThrottle):
    scope = 'chatbot'