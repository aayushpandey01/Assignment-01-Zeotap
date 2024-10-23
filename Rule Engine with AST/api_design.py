import json
import sqlite3

class Node:
    def __init__(self, type, left=None, right=None, value=None):
        self.type = type
        self.left = left
        self.right = right
        self.value = value
        

    def to_dict(self):
        return {
            "type": self.type,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None,
            "value": self.value
        }

class RuleEngine:
    def __init__(self, db_path='rules.db'):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS rules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rule_string TEXT NOT NULL,
                    ast_json TEXT NOT NULL
                )
            """)

    def create_rule(self, rule_string):
        
        node = self._parse_rule(rule_string)
        ast_json = json.dumps(node.to_dict())
        with self.conn:
            self.conn.execute("INSERT INTO rules (rule_string, ast_json) VALUES (?, ?)", (rule_string, ast_json))
        return node

    def _parse_rule(self, rule_string):
        
        return Node('operator', value='AND', left=Node('operand', value='age > 30'), right=Node('operand', value='department == "Sales"'))

    def combine_rules(self, rules):
       
        combined_ast = Node('operator', value='AND', left=rules[0], right=rules[1])
        return combined_ast

    def evaluate_rule(self, ast_json, user_data):
        ast = self._from_json(ast_json)
        return self._evaluate_node(ast, user_data)

    def _evaluate_node(self, node, user_data):
        if node.type == 'operand':
            return eval(node.value, {}, user_data)
        elif node.type == 'operator':
            left_value = self._evaluate_node(node.left, user_data)
            right_value = self._evaluate_node(node.right, user_data)
            if node.value == 'AND':
                return left_value and right_value
            elif node.value == 'OR':
                return left_value or right_value

    def _from_json(self, ast_json):
        
        return json.loads(ast_json, object_hook=lambda d: Node(**d))

engine = RuleEngine()
rule1 = engine.create_rule("age > 30 AND department == 'Sales'")
rule2 = engine.create_rule("age < 25 AND department == 'Marketing'")
combined_rule = engine.combine_rules([rule1, rule2])
user_data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
result = engine.evaluate_rule(json.dumps(combined_rule.to_dict()), user_data)
print(result)

rule_string = "age > 30 AND department == 'Sales'"
rule = engine.create_rule(rule_string)
assert rule.to_dict() == {
    "type": "operator",
    "left": {
        "type": "operand",
        "value": "age > 30",
        "left": None,
        "right": None
    },
    "right": {
        "type": "operand",
        "value": "department == 'Sales'",
        "left": None,
        "right": None
    },
    "value": "AND"
}

combined_rule = engine.combine_rules([rule1, rule2])
assert combined_rule.to_dict() == {
    "type": "operator",
    "left": rule1.to_dict(),
    "right": rule2.to_dict(),
    "value": "AND"
}

user_data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
result = engine.evaluate_rule(json.dumps(combined_rule.to_dict()), user_data)
assert result == True
