## directory structure

```
.
|-- README.md
|-- contexts
|   |-- contexts.json
|   |-- contexts.txt
|   |-- contexts_modified.json
|   `-- utt_id
`-- recog.txt

1 directory, 6 files
```

### Get recognition results for AIshell




### Extract NERs

```
python ../../scripts/extract_contexts.py --recog-result recog.txt --lang CN --output contexts/contexts.json
```


### Get contexts list and utterance ids

```
python ../../scripts/get_contexts_list.py --manifest contexts/contexts_modified.json --output-dir contexts 
```


