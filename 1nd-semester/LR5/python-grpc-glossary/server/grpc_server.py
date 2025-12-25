class GlossaryData:
    def __init__(self):
        self.terms = [
            {
                "id": 1,
                "term": "Переменная",
                "definition": "Именованная область памяти для хранения данных",
                "category": "basic",
                "examples": "x = 5\nname = 'Python'"
            },
            {
                "id": 2,
                "term": "Функция",
                "definition": "Блок кода, выполняющий определенную задачу",
                "category": "basic", 
                "examples": "def greet(name):\n    return f'Hello {name}'"
            },
            # ... 40+ терминов как в предыдущем примере
        ]
        self.next_id = len(self.terms) + 1
    
    def get_all_terms(self):
        return self.terms
    
    def get_term(self, term_id):
        return next((term for term in self.terms if term["id"] == term_id), None)
    
    def search_terms(self, query):
        query = query.lower()
        return [term for term in self.terms 
                if query in term["term"].lower() 
                or query in term["definition"].lower()]
    
    def add_term(self, term, definition, category="general", examples=""):
        new_term = {
            "id": self.next_id,
            "term": term,
            "definition": definition,
            "category": category,
            "examples": examples
        }
        self.terms.append(new_term)
        self.next_id += 1
        return new_term
    
    def update_term(self, term_id, term, definition, category, examples):
        for i, t in enumerate(self.terms):
            if t["id"] == term_id:
                self.terms[i] = {
                    "id": term_id,
                    "term": term,
                    "definition": definition,
                    "category": category,
                    "examples": examples
                }
                return self.terms[i]
        return None
    
    def delete_term(self, term_id):
        self.terms = [term for term in self.terms if term["id"] != term_id]
        return True