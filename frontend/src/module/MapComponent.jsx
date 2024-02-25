import React, { useEffect,useState } from 'react';
import Map from '@arcgis/core/Map';
import MapView from '@arcgis/core/views/MapView';
import Graphic from '@arcgis/core/Graphic';
import GraphicsLayer from '@arcgis/core/layers/GraphicsLayer';
import esriConfig from '@arcgis/core/config';
import PopupTemplate from '@arcgis/core/PopupTemplate';

import mapConfig from './config/mapConfig';

import './css/map.css';


const MapComponent = ({points}) => {
  const [graphicsLayer, setGraphicsLayer] = useState(null);

  useEffect(() => {
    esriConfig.apiKey = process.env.REACT_APP_ARCGIS_API_KEY;

    const map = new Map({
      basemap: mapConfig.basemap // Note the change in basemap string
    });

    const view = new MapView({
      container: 'map-container',
      map: map,
      center: mapConfig.center,
      zoom: mapConfig.zoom,
    });

    const layer = new GraphicsLayer();
    map.add(layer);
    setGraphicsLayer(layer);
    return () => {
      if (view) {
        // Destroy the map view
        view.container = null;
      }
    };
  }, []);



  
  useEffect(() => {
    if (!graphicsLayer || !points) return;

    graphicsLayer.removeAll();

    points.forEach(point => {
      const { longitude, latitude, sample_date, description } = point;
      const attributes = {
      name: "Point",
      description: description,
      sample_date:  sample_date
      }
      const pointGraphic = new Graphic({

        geometry: {
          type: 'point',
          longitude,
          latitude
        },
        symbol: {
          type: 'simple-marker',
          color: [226, 119, 40], // Orange
          outline: {
            color: [255, 255, 255], // White
            width: 1,
          },
          size: "8px" 

        },
        attributes: attributes
      });
      
      graphicsLayer.add(pointGraphic);

    });

    graphicsLayer.popupTemplate = new PopupTemplate({
      title: "{name}",
      content: [{
        type: "fields",
        fieldInfos: [
          {
            fieldName: "description",
            label: "Description"
          },
          {
            fieldName: "sample_date",
            label: "Sample Date"
          }
        ]
      }]
    });


  }, [points, graphicsLayer]);




  return (
    <div id="map-app-content">
      <div id="map-container" style={{height: '100%', width: '100%'}}>
      </div>
    </div>
  );
};

export default MapComponent;
