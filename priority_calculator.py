# priority_calculator.py

def tokenize_expression(expression):
    """
    수식을 토큰(숫자, 연산자, 괄호)으로 분리해서 리스트로 만드는 함수
    예: "( 4 + 5 ) * 3" → ['(', '4', '+', '5', ')', '*', '3']
    """
    tokens = []  # 분리된 토큰들을 저장할 리스트
    i = 0  # 현재 읽고 있는 문자 위치
    
    while i < len(expression):
        if expression[i].isspace():  # 공백이면 건너뛰기
            i += 1
            continue
        elif expression[i] in '()+-*/':  # 괄호나 연산자면
            tokens.append(expression[i])  # 그대로 리스트에 추가
            i += 1
        elif expression[i].isdigit() or expression[i] == '.':  # 숫자나 소수점이면
            # 숫자를 완전히 읽을 때까지 계속 읽기
            num = ''
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                num += expression[i]
                i += 1
            tokens.append(num)  # 완성된 숫자를 리스트에 추가
        else:
            # 이상한 문자가 있으면 에러
            raise ValueError("Invalid character")
    
    return tokens

def find_innermost_parentheses_in_list(tokens):
    """
    리스트에서 가장 안쪽 괄호의 위치를 찾는 함수
    예: ['(', '4', '+', '(', '5', '*', '2', ')', ')'] 에서 
        (5*2) 부분인 인덱스 3~7을 찾기
    """
    start = -1  # 가장 최근에 만난 '(' 위치
    
    for i in range(len(tokens)):
        if tokens[i] == '(':  # 여는 괄호를 만나면
            start = i  # 위치 기록 (더 안쪽이 있을 수 있으므로 계속 업데이트)
        elif tokens[i] == ')':  # 닫는 괄호를 만나면
            if start != -1:  # 짝이 맞는 여는 괄호가 있다면
                return start, i  # 가장 안쪽 괄호의 시작과 끝 반환
    
    return None, None  # 괄호가 없으면 None 반환

def calculate_without_parentheses(tokens):
    """
    괄호가 없는 토큰 리스트를 계산하는 함수
    연산자 우선순위 적용: *, / 먼저 계산하고 +, - 나중에 계산
    예: ['4', '+', '5', '*', '3'] → ['4', '+', '15'] → ['19']
    """
    # 모든 토큰을 숫자로 변환 (연산자 제외)
    result_tokens = []
    for token in tokens:
        if token in '+-*/':
            result_tokens.append(token)  # 연산자는 그대로
        else:
            result_tokens.append(float(token))  # 숫자는 float로 변환
    
    # 1단계: 곱셈(*), 나눗셈(/) 먼저 처리
    i = 1  # 연산자는 홀수 인덱스에 있음
    while i < len(result_tokens):
        if result_tokens[i] == '*':  # 곱셈 발견
            # 앞 숫자 * 뒤 숫자
            result = result_tokens[i-1] * result_tokens[i+1]
            # 3개 요소(숫자, *, 숫자)를 결과 1개로 교체
            result_tokens = result_tokens[:i-1] + [result] + result_tokens[i+2:]
            # i는 그대로 (리스트가 줄어들었으므로)
        elif result_tokens[i] == '/':  # 나눗셈 발견
            if result_tokens[i+1] == 0:  # 0으로 나누기 체크
                raise ZeroDivisionError("Division by zero")
            result = result_tokens[i-1] / result_tokens[i+1]
            result_tokens = result_tokens[:i-1] + [result] + result_tokens[i+2:]
        else:
            i += 2  # 다음 연산자로 이동
    
    # 2단계: 덧셈(+), 뺄셈(-) 처리
    i = 1
    while i < len(result_tokens):
        if result_tokens[i] == '+':  # 덧셈 발견
            result = result_tokens[i-1] + result_tokens[i+1]
            result_tokens = result_tokens[:i-1] + [result] + result_tokens[i+2:]
        elif result_tokens[i] == '-':  # 뺄셈 발견
            result = result_tokens[i-1] - result_tokens[i+1]
            result_tokens = result_tokens[:i-1] + [result] + result_tokens[i+2:]
        else:
            i += 2
    
    # 최종적으로 결과 하나만 남음
    return result_tokens[0]

def calculate_expression(expression):
    """
    괄호를 단계적으로 처리하여 계산하는 메인 함수
    """
    try:
        # 1단계: 수식을 토큰 리스트로 변환
        tokens = tokenize_expression(expression)
        # 예: "( 4 + 5 ) * 3" → ['(', '4', '+', '5', ')', '*', '3']
        
        # 2단계: 괄호가 있는 동안 계속 반복
        while '(' in tokens and ')' in tokens:
            
            # 가장 안쪽 괄호 찾기
            start, end = find_innermost_parentheses_in_list(tokens)
            
            if start is None or end is None:
                return "Invalid input."
            
            # 괄호 안의 토큰들 추출
            # 예: ['(', '4', '+', '5', ')'] 에서 start=0, end=4라면
            # inner_tokens = ['4', '+', '5'] (괄호 제외)
            inner_tokens = tokens[start+1:end]
            
            # 괄호 안의 식 계산
            inner_result = calculate_without_parentheses(inner_tokens)
            
            # 계산 결과로 괄호 부분을 교체해서 새로운 리스트 생성
            # 예: ['(', '4', '+', '5', ')', '*', '3'] → ['9.0', '*', '3']
            tokens = tokens[:start] + [str(inner_result)] + tokens[end+1:]
            
            # 이 과정을 괄호가 없어질 때까지 반복
        
        # 3단계: 괄호가 모두 사라진 후 최종 계산
        if '(' in tokens or ')' in tokens:
            return "Invalid input."
        
        final_result = calculate_without_parentheses(tokens)
        return f"Result: {final_result}"
        
    except ZeroDivisionError:
        return "Error: Division by zero."
    except (ValueError, IndexError):
        return "Invalid input."

def main():
    """
    메인 함수 - 프로그램 실행의 시작점
    """
    try:
        expression = input("수식을 입력해주세요: ").strip()
        print(calculate_expression(expression))
    except EOFError:
        pass

if __name__ == "__main__":
    main()
