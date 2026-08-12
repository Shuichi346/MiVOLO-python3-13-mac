
uv run mivolo-cli \
--input "jennifer_lawrence.jpg" \
--output "output" \
--detector-weights "pretrained/yolov8x_person_face.pt" \
--checkpoint "pretrained/checkpoint-377.pth.tar" \
--device "auto" \
--draw \
--with-persons

uv run mivolo-cli \
--input "https://www.youtube.com/shorts/pVh32k0hGEI" \
--output "output" \
--detector-weights "pretrained/yolov8x_person_face.pt" \
--checkpoint "pretrained/checkpoint-377.pth.tar" \
--device "auto" \
--draw \
--with-persons
