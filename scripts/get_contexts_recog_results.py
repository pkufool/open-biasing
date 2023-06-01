import argparse
import os

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--recog-result",
        type=str,
        help="""The recognition results, it should be the `recog-*` logs generated
        by icefall (i.e for each utterance it has both ref and hyp).
        """,
    )

    parser.add_argument(
        "--contexts-utt",
        type=str,
        help="The utt ids of context test set",
    )

    parser.add_argument(
        "--test-name",
        type=str,
        help="The name of the test set, will be the suffix of output file names",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="results",
        help="The path where the refs and hyps will write to.",
    )
    return parser.parse_args()


def main():
    args = get_args()

    assert os.path.exists(
        args.recog_result
    ), f"Recognition results : {args.recog_result} does not exist."

    assert os.path.exists(
        args.contexts_utt
    ), f"Contexts utt : {args.contexts_utt} does not exist."

    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)

    utts = set()
    with open(args.contexts_utt, "r") as f:
        for line in f.readlines():
            utts.add(line.strip())

    test_list = {}
    for line in open(args.recog_result, "r").readlines():
        utt_id, hyp_ref = line.split(":")
        if utt_id not in test_list:
            test_list[utt_id] = [None, None]
        exec(hyp_ref.strip())
        if "ref=" in hyp_ref:
            test_list[utt_id][0] = " ".join(locals()["ref"])
        if "hyp=" in hyp_ref:
            test_list[utt_id][1] = " ".join(locals()["hyp"])

    ref_f = open(f"{args.output_dir}/refs_selected_{args.test_name}.txt", "w", encoding="utf-8")
    hyp_f = open(f"{args.output_dir}/hyps_selected_{args.test_name}.txt", "w", encoding="utf-8")
    ref_f_other = open(f"{args.output_dir}/refs_other_{args.test_name}.txt", "w", encoding="utf-8")
    hyp_f_other = open(f"{args.output_dir}/hyps_other_{args.test_name}.txt", "w", encoding="utf-8")
    for k, v in test_list.items():
        if k in utts:
            ref_f.write(f"{k}\t{v[0]}\n")
            hyp_f.write(f"{k}\t{v[1]}\n")
        else:
            ref_f_other.write(f"{k}\t{v[0]}\n")
            hyp_f_other.write(f"{k}\t{v[1]}\n")

    ref_f.flush()
    hyp_f.flush()
    ref_f_other.flush()
    hyp_f_other.flush()
    ref_f.close()
    hyp_f.close()
    ref_f_other.close()
    hyp_f_other.close()

if __name__ == "__main__":
    main()
