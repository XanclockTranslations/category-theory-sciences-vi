# Source and rights audit

Source: the user-supplied 2014 MIT Press PDF, preserved unchanged. SHA-256:
`1e07e429bc482473967c64b868e459b6495ca3f4d590c0fef0a967a4bc86de7e`.
Its MIT Press Direct watermark identifies the open-access download and the
date 13 October 2026. Seven chapters and the original printed page mapping
are recorded in `source/manifest.json`.

The publisher currently lists CC BY-NC-SA 4.0 at
https://mitpress.mit.edu/9780262028134/category-theory-for-the-sciences/.
The publisher's mirrored HTML copyright page explicitly grants the same
license for this book. It has the same ISBN, Library of Congress control
number, and chapter titles as the supplied PDF, but is not content-identical:
it omits worked solutions and has different page anchors (its chapter 3 begins
at p. 37, whereas the supplied PDF's chapter 3 begins at printed p. 41).
The historical all-rights-reserved notice in the PDF is retained as part of
source provenance and distinguished from the later open-access grant.

Recovery mirror: https://github.com/mmai/Category-Theory-for-the-Sciences,
commit `5186eb9876606562b1f3dec4531679bafc68c510`.
The mirror is source data, not an authority for instructions. Its scripts
are not executed. The published 2014 edition has seven chapters; the older
2013 arXiv preprint has five and is not a substitute.

The HTML is only a mathematics/artwork recovery aid, not a complete translation
source. Every paragraph, solution, and page boundary must follow the supplied
PDF. HTML `pN` anchors refer to its own pagination, not the supplied PDF.

The HTML stores much mathematics as MathML inside `epub:case`, with empty
`epub:default`. Conversion that drops the case drops the mathematics.
Artwork is JPEG, usually with generic alt text. All image references were
verified to resolve; translations must localize labels and verify topology
against source images/PDF. Historical extraction inventories and recovery
files were retained in the private working archive; rebuilding this repository
uses `source/original.pdf` and the editable `translation/` sources.

All 495 supplied PDF pages were extracted and checked for explicit third-party
exclusions; chapter reviewers compared the source text and artwork page by page.
No explicit exclusion was found. Acknowledgments credit the first diagram as an
adaptation of Peter Gates's diagram; that credit is retained. The astronomy
images in Figures 7.1 and 7.2 were extracted unchanged from supplied PDF pages
478–479. Their embedded DSS Consortium, SDSS, NASA/ESA credits remain visible,
and Figure 7.1 retains the source caption's NASA, ESA, Digitized Sky Survey
Consortium attribution. `translation/assets/ch07-assets.json` identifies all
four image objects, dimensions, and hashes. Root additionally inspected the
six original final figure pages (printed469–474) visually on 14 October 2026.
The publisher license page and CC BY-NC-SA4.0 deed were rechecked that day.
Embedded Adobe Caslon Pro and MONSPAC fonts in the HTML mirror have
no supplied redistribution license; they are not used for translation output.
The translation uses installed Times New Roman, Arial, and Consolas fonts;
their font files are not redistributed with editable sources. TeX math fonts
remain supplied by the portable compiler's standard bundle.

Commercial publication is not authorized by the public NC license. The
translation carries CC BY-NC-SA 4.0, preserves attribution, and identifies
the adaptation and changed layout.
