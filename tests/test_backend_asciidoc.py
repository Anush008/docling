import glob
import os
from pathlib import Path

import pytest
from docling_core.types.doc import BoundingBox

from docling.backend.asciidoc_backend import AsciidocBackend
from docling.datamodel.base_models import InputFormat
from docling.datamodel.document import InputDocument


def _get_backend(fname):
    in_doc = InputDocument(
        path_or_stream=fname,
        format=InputFormat.ASCIIDOC,
        backend=AsciidocBackend,
    )

    doc_backend = in_doc._backend
    return doc_backend


def test_asciidocs_examples():

    fnames = sorted(glob.glob("./tests/data/*.asciidoc"))

    for fname in fnames:
        print(f"reading {fname}")

        bname = os.path.basename(fname)
        gname = os.path.join("./tests/data/groundtruth/docling_v2/", bname + ".md")

        doc_backend = _get_backend(Path(fname))
        doc = doc_backend.convert()

        pred_mddoc = doc.export_to_markdown()

        if os.path.exists(gname):
            with open(gname, "r") as fr:
                true_mddoc = fr.read()

            assert pred_mddoc == true_mddoc, "pred_mddoc!=true_mddoc for asciidoc"
        else:
            with open(gname, "w") as fw:
                fw.write(pred_mddoc)

            print("\n\n", doc.export_to_markdown())