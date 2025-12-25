import grpc
from concurrent import futures
import glossary_pb2
import glossary_pb2_grpc
from glossary_data import GlossaryData

class GlossaryServicer(glossary_pb2_grpc.GlossaryServiceServicer):
    def __init__(self):
        self.glossary = GlossaryData()
    
    def GetTerm(self, request, context):
        term = self.glossary.get_term(request.id)
        if term:
            return glossary_pb2.TermResponse(
                term=glossary_pb2.Term(**term),
                success=True,
                message="Term found"
            )
        return glossary_pb2.TermResponse(
            success=False,
            message="Term not found"
        )
    
    def GetAllTerms(self, request, context):
        terms = self.glossary.get_all_terms()
        return glossary_pb2.TermsResponse(
            terms=[glossary_pb2.Term(**term) for term in terms],
            success=True,
            message=f"Found {len(terms)} terms"
        )
    
    def SearchTerms(self, request, context):
        terms = self.glossary.search_terms(request.query)
        return glossary_pb2.TermsResponse(
            terms=[glossary_pb2.Term(**term) for term in terms],
            success=True,
            message=f"Found {len(terms)} matching terms"
        )
    
    def AddTerm(self, request, context):
        new_term = self.glossary.add_term(
            request.term,
            request.definition,
            request.category,
            request.examples
        )
        return glossary_pb2.TermResponse(
            term=glossary_pb2.Term(**new_term),
            success=True,
            message="Term added successfully"
        )
    
    def UpdateTerm(self, request, context):
        updated_term = self.glossary.update_term(
            request.id,
            request.term,
            request.definition,
            request.category,
            request.examples
        )
        if updated_term:
            return glossary_pb2.TermResponse(
                term=glossary_pb2.Term(**updated_term),
                success=True,
                message="Term updated successfully"
            )
        return glossary_pb2.TermResponse(
            success=False,
            message="Term not found"
        )
    
    def DeleteTerm(self, request, context):
        success = self.glossary.delete_term(request.id)
        return glossary_pb2.Empty()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    glossary_pb2_grpc.add_GlossaryServiceServicer_to_server(GlossaryServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC Server running on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()