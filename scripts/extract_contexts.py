import argparse
import logging
import json
import os
import sys

import spacy


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
        "--lang",
        type=str,
        help="The language, could either be EN or CN",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="contexts/contexts.json",
        help="The path where the final result will write to.",
    )
    return parser.parse_args()


def main():
    args = get_args()
    logging.info(f"Loading NER model for {args.lang}...")
    if args.lang == "EN":
        nlp = spacy.load("en_core_web_trf")
    else:
        assert args.lang == "CN", f"Only EN and CN are supported, given {args.lang}"
        nlp = spacy.load("zh_core_web_trf")
    logging.info(f"Loading NER model done.")

    assert os.path.exists(
        args.recog_result
    ), f"Recognition results : {args.recog_result} does not exist."

    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    logging.info(f"Parsing recognition results.")
    ifile = args.recog_result
    delimeter = " " if args.lang == "EN" else ""
    test_list = {}
    for line in open(ifile, "r").readlines():
        utt_id, hyp_ref = line.split(":")
        if utt_id not in test_list:
            test_list[utt_id] = [None, None]
        exec(hyp_ref.strip())
        if "ref=" in hyp_ref:
            test_list[utt_id][0] = delimeter.join(locals()["ref"])
        if "hyp=" in hyp_ref:
            test_list[utt_id][1] = delimeter.join(locals()["hyp"])

    logging.info(f"Parsing and selecting NER.")
    results = {}
    count = 0
    for k, v in test_list.items():
        count += 1
        if count % 200 == 0:
            logging.info(f"{count} / {len(test_list)} items have been processed.")

        doc = nlp(v[0].strip())
        ner = [(x.text, x.label_) for x in doc.ents]
        if ner:
            ner_items = set([x[0] for x in ner])
            hit_ners = []
            for x in ner_items:
                if x in v[0] and x not in v[1]:
                    hit_ners.append(x)
            if hit_ners:
                results[k] = {}
                results[k]["contexts"] = hit_ners
                results[k]["ref"] = v[0]
        else:
            continue
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    logging.info(f"Processing done.")


if __name__ == "__main__":
    formatter = "%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=formatter,
    )

    main()
