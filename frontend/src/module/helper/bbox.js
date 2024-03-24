import SimpleFillSymbol from '@arcgis/core/symbols/SimpleFillSymbol';
import Graphic from '@arcgis/core/Graphic';

const drawBoundingBoxes = (graphicsLayer, boundingBoxes) => {
    boundingBoxes.forEach(box => {
      const { coordinates } = box;
      const [xMin, yMin, xMax, yMax] = coordinates;
      const polygon = {
        type: "polygon",
        rings: [
          [xMin, yMin],
          [xMin, yMax],
          [xMax, yMax],
          [xMax, yMin],
          [xMin, yMin]
        ]
      };

      const boundingBoxSymbol = new SimpleFillSymbol({
        color: [227, 139, 79, 0.2],  // Semi-transparent fill
        outline: {
          color: [255, 255, 255],  // White outline
          width: 1
        }
      });

      const polygonGraphic = new Graphic({
        geometry: polygon,
        symbol: boundingBoxSymbol
      });

      graphicsLayer.add(polygonGraphic);
    });
};

export { drawBoundingBoxes };
