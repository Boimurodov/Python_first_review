import sys

from encode_and_decode import code_and_decode
from hack_and_train import hack, train
from hack_vigenere import hack_vigenere
import parser


def main():
    args = parser.command_parser.parse_args()
    if args.method == 'encode':
        code_and_decode(args.cipher, args.key, args.input_file, args.output_file, is_encode=True)
    elif args.method == 'decode':
        code_and_decode(args.cipher, args.key, args.input_file, args.output_file, is_encode=False)
    elif args.method == 'train':
        train(args.text_file, args.model_file)
    elif args.method == 'hack':
        hack(args.input_file, args.output_file, args.model_file)
    elif args.method == 'hack_vigenere':
        hack_vigenere(args.input_file, args.output_file, args.model_file)
    # if sys.argv[1] == 'encode':
    #    code_and_decode(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5],
    #                    is_encode=True)
    # if sys.argv[1] == 'decode':
    #    code_and_decode(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5],
    #                    is_encode=False)
    # if sys.argv[1] == 'train':
    #    train(sys.argv[2], sys.argv[3])
    # if sys.argv[1] == 'hack':
    #    hack(sys.argv[2], sys.argv[3], sys.argv[4])
    # if sys.argv[1] == 'hack_vigenere':
    #    hack_vigenere(sys.argv[2], sys.argv[3], sys.argv[4])


if __name__ == '__main__':
    main()
