"use strict";

class PdfEditorData extends EditorDataBase {

    constructor(elem, name, path, container_selector = ".editor-content", editor_options = {}) {
        super(elem, name, path, container_selector, editor_options);
        this.editor_type = 'pdf';
        this.viewer = null;


        this.dom_canvas = elem_from_tag("canvas", "");
        this.editor_container.appendChild(this.dom_canvas);

        // this.dom_canvas.style.width = "100%";
        // this.dom_canvas.style.height = "100%";

        // /** @type {CanvasUserInterface} */
        this.canvas = this.dom_canvas.getContext('2d');

        this.pdf_loader = pdfjsLib.getDocument("/api/load_pdf");
        this.pdf_loader.promise.then(function(pdf) {
          // you can now use *pdf* here
            pdf.getPage(1).then(function(page) {
              // you can now use *page* here
                let scale = 1.5;
                let viewport = page.getViewport({ scale: scale, });

                // let canvas = document.getElementById('the-canvas');
                // let context = canvas.getContext('2d');
                this.dom_canvas.height = viewport.height;
                this.dom_canvas.width = viewport.width;

                let renderContext = {
                  canvasContext: context,
                  viewport: viewport
                };
                page.render(renderContext);

            });
        });
    }

}

