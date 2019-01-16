#!/usr/bin/env python3
"""Converts the CALBC corpus (in IeXML format) to Standoff format.

Run the script with:

```
python iexml_to_standoff.py path/to/corpus/in/IeXML/format
```

e.g.

```
python iexml_to_standoff.py -i path/to/CALBC -o ~/Desktop/CALBC_s
```

Note: the script will just skip articles whenever an error occurs or something fishy happens.
Therefore, the number of output articles will be less than the number of input articles.

Resources:

- Useful app for checking regex: https://regex101.com
"""
import argparse
import errno
import os
import random
import re
import xml.etree.ElementTree as ET

START = '<ENTITY_START>'
END = '<ENTITY_END>'

# https://stackoverflow.com/questions/273192/how-can-i-create-a-directory-if-it-does-not-exist#273227
def make_dir(dir_path):
    """Creates a directory (directory_filepath) if it does not exist.

    Args:
        directory_filepath: filepath of directory to create
    """
    # create output directory if it does not exist
    try:
        os.makedirs(dir_path)
    except OSError as err:
        if err.errno != errno.EEXIST:
            raise

def parse_iexml(filepath):
    """Yields string representations of each XML document in the IeXML file at `filepath`.
    Args:
        filepath (str): filepath to IeXML file to parse.
    Yields:
        the next XML representation of an artcile in the IeXML corpus as `filepath`.
    """
    with open(filepath, 'r') as f:
        file_contents = f.read()

    corpus = file_contents.split('<PubmedArticle>')
    # add back delimiter, remove spurious first element of split
    for xml in corpus[1:]:
        yield '<PubmedArticle>' + xml

def get_root(xml):
    """Returns the root of a given XML file, `xml` encoded as a string.

    Args:
        xml (str): XML file, represented as a string.

    Returns:
        root of the XML, `xml`.
    """
    try:
        root = ET.fromstring(xml)
    except ET.ParseError as err:
        print('[ERROR] Parse error: {}'.format(err.args[0]))
    else:
        return root

def get_pmid(root):
    """Returns the PubMed Identifier (PMID) XML at `root`.
    Args:
        root (ElementTree): root of an XML.

    Returns:
        <Article></Article> element of the XML at `root`
    """
    return root.find('MedlineCitation').find('PMID').text

def get_abstract_sents(root):
    """Return <ArticleTitle></ArticleTitle> element for a given `article`.

    Args:
        root (ElementTree): root of an XML.

    Returns:
        <ArticleTitle></ArticleTitle> element for a given `article`
    """
    title = None
    body = None
    try:
        title = root.find('MedlineCitation').find('Article').find('ArticleTitle').find('document')
        body = root.find('MedlineCitation').find('Article').find('Abstract').find('AbstractText').find('document')
    except AttributeError as e:
        print('[ERROR] Error processing article with PMID: {} ({})'.format(get_pmid(root), e))
    return title, body

def get_article(root):
    """Returns a dictionary containing information from the article at `root`.

    For the XML rooted at `root`, which represents a single PubMed article, collects all the
    information neccecary to convert the article to Standoff format, and returns this in as a
    dictionary. Returns None if an error was encountered when extracting the abstract text.

    Args:
        root (ElementTree): root of an XML.

    Returns:
        a dictionary containing all information from the article in XML format at `root` needed
        to convert the article to Standoff format, None if an error was encountered extracting the
        articles text.
    """
    pmid = get_pmid(root)
    abstract_title_sents, abstract_body_sents = get_abstract_sents(root)
    if abstract_body_sents is None:
        return None
    else:
        article = {'pmid': pmid,
                   'title_sents': abstract_title_sents,
                   'body_sents': abstract_body_sents,
                  }
    return article

def process_abtract_text(article):
    """Processes all the text from the <ArticleTitle> and <AbstractText> elements of `article` XML

    For the title and abstract body text of a PubMed article represented as an XML (`article`),
    removes all XML tags and replaces entity tags.

    Args:
        article (str): string representation of an XML, represents a single PubMed article.

    Returns:
        a string containing the concatenated text from an articles title and abstract text.
    """
    # get a concatenated string representation of abstract title/body text
    abstract_title_text = ET.tostring(article['title_sents']).decode('utf-8')
    abstract_body_text = ET.tostring(article['body_sents']).decode('utf-8')
    text = abstract_title_text + abstract_body_text

    # get a list of the entity types
    entities = re.findall(r'''(\S+)=[\"']?((?:.(?![\"']?\s+(?:\S+)=|[>\"']))+.)[\"']?''', text)
    # clean entities
    entities = [ent[-1].upper() for ent in entities if ent[0] == 'ct']
    # automatically resolve entities annotated for two types by choosing the winner randomly!
    # this essentially introduces a small amount of random noise into the training data, which
    # shouldn't be a problem for a DNN
    entities = [random.choice(ent.split('|')) for ent in entities]

    # remove document tags
    processed_text = re.sub(r'</?document[^>]*>', '', text)
    # remove sentence tags
    processed_text = re.sub(r'<s[^>]*>', '', processed_text)
    processed_text = re.sub(r'</s[^>]*>', ' ', processed_text)
    # convert all entity tags to special START and END tokens
    processed_text = re.sub(r'<e[^>]*>', START, processed_text)
    processed_text = re.sub(r'</e[^>]*>', END, processed_text)
    processed_text = processed_text.strip()

    return processed_text, entities

def get_label_offsets(text):
    """Given some annotated `text`, returns the start and end offsets of each annotation.

    For some `test`, where annotatations are marked by the special START and END markers, return
    a list of tuples which contain the (start, end) offsets in `text` of each annotation.

    Args:
        text: annotated text marked up for entities with special START and END markers.

    Returns:
        a list of character offsets for each annotated entity in `text`.
    """
    offsets = []
    start_search_idx = 0
    while True:
        # find start of entity offset, remove START tag
        start_offset = text.find(START, start_search_idx)
        # if we don't find a START tag, break the loop
        if start_offset < 0:
            break
        text = re.sub(START, '', text, count=1)

        # find end of entity offset, remove END tag
        end_offset = text.find(END)
        text = re.sub(END, '', text, count=1)

        offsets.append((start_offset, end_offset))

        # update counter
        start_search_idx = end_offset

    return offsets

def write_text_file(filename, text, output_dir):
    """Writes string `text` to file `filename`.

    Args:
        filename (str): path to file to write `text` to.
        text (str): text to write to file at `filename`.
    """
    filename = os.path.join(output_dir, filename)
    with open(filename, 'w') as f:
        f.write(text)

def write_ann_file(filename, ents, output_dir):
    """Writes elements of list `ents` to file `filename`, one line per element

    Args:
        filename (str): path to file to write `text` to.
        ents (list): list of strings to write to file at `filename`, one element per line.
    """
    filename = os.path.join(output_dir, filename)
    with open(filename, 'w') as f:
        for ent in ents:
            f.write(ent)

def iexml_to_standoff(filepath, output_dir):
    """Coordinates the conversion of a corpus at `filepath` in IeXML format to Standoff format
    """
    for xml in parse_iexml(filepath):
        root = get_root(xml)
        article = get_article(root)

        # None occurs when we couldnt extract the abstracts text, so skip this article
        if article is None:
            continue

        # remove XML tags, label entities with special START and END tags
        abstract_body, entities = process_abtract_text(article)
        # get all label offsets
        label_offsets = get_label_offsets(abstract_body)

        # TEMP: weird bug where # of entities doesn't equal # of offsets, skip for now
        if len(entities) != len(label_offsets):
            print('[ERROR] Error processing article with PMID: {}'.format(get_pmid(root)))
            continue

        # strip special START and END tags once label offsets are found
        abstract_body = re.sub(START, '', abstract_body)
        abstract_body = re.sub(END, '', abstract_body)

        # write text file (`.txt`)
        text_filename = '{}.txt'.format(article['pmid'])
        write_text_file(text_filename, abstract_body, output_dir)

        # write ann file (`.ann`)
        ann = []
        for term_count, offset in enumerate(label_offsets):
            start, end = offset[0], offset[-1]
            ent_label = entities[term_count]
            ent_text = abstract_body[start:end]

            ann.append('T{}\t{} {} {}\t{}\n'.format(term_count + 1, ent_label, start, end, ent_text))
            ann_file = '{}.ann'.format(article['pmid'])
            write_ann_file(ann_file, ann, output_dir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert corpus in IeXML format to Standoff format.')
    parser.add_argument('-i', '--input', type=str, required=True, help='Filepath to the IeXML formatted corpus.')
    parser.add_argument('-o', '--output', type=str, required=True, help='Directory to save Standoff formated corpus.')
    args = parser.parse_args()

    make_dir(args.output)
    iexml_to_standoff(args.input, args.output)
