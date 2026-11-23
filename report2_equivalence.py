A = [1, 2, 3, 4, 5]
N = len(A)


def print_matrix(matrix, title):
    """관계행렬을 보기 쉬운 형태로 출력한다."""
    print("\n" + title)
    print("    " + " ".join(str(x) for x in A))
    print("   " + "----" * N)
    for i, row in enumerate(matrix):
        print(f"{A[i]} | " + "  ".join(str(value) for value in row))


def input_relation_matrix():
    """사용자로부터 5x5 0-1 관계행렬을 입력받는다."""
    print("집합 A = {1, 2, 3, 4, 5}")
    print("관계행렬의 각 행을 0 또는 1로 입력하세요.")
    print("예: 1 0 0 1 0")

    matrix = []
    for i in range(N):
        while True:
            try:
                values = list(map(int, input(f"{i + 1}행 입력: ").split()))
                if len(values) != N:
                    print("오류: 각 행에는 숫자 5개를 입력해야 합니다.")
                elif any(value not in (0, 1) for value in values):
                    print("오류: 행렬 원소는 0 또는 1만 가능합니다.")
                else:
                    matrix.append(values)
                    break
            except ValueError:
                print("오류: 정수 0 또는 1로 입력하세요.")
    return matrix


def is_reflexive(matrix):
    """모든 대각 원소가 1인지 검사한다."""
    for i in range(N):
        if matrix[i][i] != 1:
            return False
    return True


def is_symmetric(matrix):
    """모든 i, j에 대해 M[i][j] = M[j][i]인지 검사한다."""
    for i in range(N):
        for j in range(N):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True


def is_transitive(matrix):
    """M[i][j]=1이고 M[j][k]=1이면 M[i][k]=1인지 검사한다."""
    for i in range(N):
        for j in range(N):
            if matrix[i][j] == 1:
                for k in range(N):
                    if matrix[j][k] == 1 and matrix[i][k] == 0:
                        return False
    return True


def check_relation(matrix, title="관계 판별 결과"):
    """세 가지 성질과 동치 관계 여부를 출력하고 결과를 반환한다."""
    reflexive = is_reflexive(matrix)
    symmetric = is_symmetric(matrix)
    transitive = is_transitive(matrix)

    print(f"\n[{title}]")
    print(f"반사성(Reflexive): {'만족' if reflexive else '불만족'}")
    print(f"대칭성(Symmetric): {'만족' if symmetric else '불만족'}")
    print(f"추이성(Transitive): {'만족' if transitive else '불만족'}")

    equivalent = reflexive and symmetric and transitive
    if equivalent:
        print("결과: 주어진 관계는 동치 관계입니다.")
    else:
        print("결과: 주어진 관계는 동치 관계가 아닙니다.")
    return equivalent


def print_equivalence_classes(matrix):
    """동치 관계의 각 원소에 대한 동치류를 출력한다."""
    if not (is_reflexive(matrix) and is_symmetric(matrix)
            and is_transitive(matrix)):
        print("동치 관계가 아니므로 동치류를 출력할 수 없습니다.")
        return

    printed = set()
    print("\n[동치류 출력]")
    for i in range(N):
        if A[i] not in printed:
            equivalence_class = {
                A[j] for j in range(N) if matrix[i][j] == 1
            }
            printed.update(equivalence_class)
            members = ", ".join(str(x) for x in sorted(equivalence_class))
            print(f"[{A[i]}] = {{{members}}}")


def reflexive_closure(matrix):
    """대각 원소를 모두 1로 만들어 반사 폐포를 구한다."""
    result = [row[:] for row in matrix]
    for i in range(N):
        result[i][i] = 1
    return result


def symmetric_closure(matrix):
    """M과 M의 전치행렬의 합집합으로 대칭 폐포를 구한다."""
    result = [row[:] for row in matrix]
    for i in range(N):
        for j in range(N):
            if matrix[i][j] == 1:
                result[j][i] = 1
    return result


def transitive_closure(matrix):
    """Warshall 알고리즘으로 추이 폐포를 구한다."""
    result = [row[:] for row in matrix]
    for k in range(N):
        for i in range(N):
            for j in range(N):
                if result[i][k] == 1 and result[k][j] == 1:
                    result[i][j] = 1
    return result


def show_closure(title, closure_function, matrix):
    """폐포 전후의 행렬과 변환 후 성질을 출력한다."""
    print("\n" + "=" * 50)
    print(title)
    print_matrix(matrix, "폐포 변환 전")
    result = closure_function(matrix)
    print_matrix(result, "폐포 변환 후")
    check_relation(result, title + " 적용 후 판별")
    print_equivalence_classes(result)
    return result


def equivalence_closure(matrix):
    """세 폐포를 적용하여 가장 작은 동치 관계를 만든다."""
    result = reflexive_closure(matrix)
    result = symmetric_closure(result)
    result = transitive_closure(result)
    return result


def main():
    print("=" * 50)
    print("동치 관계 판별 및 동치류 출력 프로그램")
    print("=" * 50)

    relation = input_relation_matrix()
    print_matrix(relation, "입력한 관계행렬")

    is_equivalence = check_relation(relation, "원래 관계 판별")
    if is_equivalence:
        print_equivalence_classes(relation)

    # 조건 4: 각 폐포를 개별적으로 계산하고 전후 행렬을 비교한다.
    show_closure("1. 반사 폐포(Reflexive Closure)",
                 reflexive_closure, relation)
    show_closure("2. 대칭 폐포(Symmetric Closure)",
                 symmetric_closure, relation)
    show_closure("3. 추이 폐포(Transitive Closure)",
                 transitive_closure, relation)

    # 추가 기능: 원래 관계를 포함하는 최소 동치 관계 계산
    print("\n" + "=" * 50)
    print("[추가 기능: 최소 동치 폐포]")
    print_matrix(relation, "변환 전 원래 관계")
    final_relation = equivalence_closure(relation)
    print_matrix(final_relation, "변환 후 최소 동치 폐포")
    check_relation(final_relation, "최소 동치 폐포 최종 검증")
    print_equivalence_classes(final_relation)

    print("\n프로그램이 정상적으로 종료되었습니다.")


if __name__ == "__main__":
    main()
