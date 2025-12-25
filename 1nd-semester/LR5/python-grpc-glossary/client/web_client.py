from flask import Flask, render_template, request, jsonify
import grpc
import glossary_pb2
import glossary_pb2_grpc

app = Flask(__name__)

def get_grpc_stub():
    channel = grpc.insecure_channel('grpc-server:50051')
    return glossary_pb2_grpc.GlossaryServiceStub(channel)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/terms')
def get_terms():
    try:
        stub = get_grpc_stub()
        response = stub.GetAllTerms(glossary_pb2.Empty())
        return jsonify({
            'success': response.success,
            'terms': [{
                'id': term.id,
                'term': term.term,
                'definition': term.definition,
                'category': term.category,
                'examples': term.examples
            } for term in response.terms]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/terms/<int:term_id>')
def get_term(term_id):
    try:
        stub = get_grpc_stub()
        response = stub.GetTerm(glossary_pb2.TermRequest(id=term_id))
        if response.success:
            return jsonify({
                'success': True,
                'term': {
                    'id': response.term.id,
                    'term': response.term.term,
                    'definition': response.term.definition,
                    'category': response.term.category,
                    'examples': response.term.examples
                }
            })
        return jsonify({'success': False, 'error': 'Term not found'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/search')
def search_terms():
    query = request.args.get('q', '')
    try:
        stub = get_grpc_stub()
        response = stub.SearchTerms(glossary_pb2.SearchRequest(query=query))
        return jsonify({
            'success': response.success,
            'terms': [{
                'id': term.id,
                'term': term.term,
                'definition': term.definition,
                'category': term.category,
                'examples': term.examples
            } for term in response.terms]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)