import models
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cau", required=True, help='Câu b, c, d')
    # parser.add_argument("-i", "--input", required=True, help='Đường dẫn đên input file')
    # parser.add_argument("-o", "--output", required=True, help='Đường dẫn đên output file')
    args = parser.parse_args()

    questions = []
    with open('./input/input.txt', 'r') as fp:
        for question in fp:
            questions.append(question)

    out = []
    for question in questions:
        string = models.Tokenize(question).parse()
        parser = models.MaltParser(models.ruleTable)
        tree = parser.parse(string)
        query = models.QueryLogic(tree)
        query.parse()

        if args.cau == "b":
            logical = models.LogicalFormParser(tree)
            out.append(logical.parse())
        elif args.cau == "c":
            out.append(query.produceQuery())
        elif args.cau == "d":
            out.append(query.answer(query.produceQuery()))
        elif args.cau == "a":
            tree.printTree()
            out.append("\n".join(tree.getTree()))
        else:
            raise Exception("Don't support cau = {}".format(args.cau))

        outputFile = './output/output_{}.txt'.format(args.cau)
        with open(outputFile, "w") as fp:
            for q, r in zip(questions, out):
                fp.writelines(q + "\n")
                fp.writelines(str(r) + "\n\n")

if __name__ == "__main__":
    main()

