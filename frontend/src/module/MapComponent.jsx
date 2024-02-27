import React, { useEffect, useState } from 'react';
import Map from '@arcgis/core/Map';
import MapView from '@arcgis/core/views/MapView';
import Graphic from '@arcgis/core/Graphic';
import GraphicsLayer from '@arcgis/core/layers/GraphicsLayer';
import esriConfig from '@arcgis/core/config';
import PopupTemplate from '@arcgis/core/PopupTemplate';

import mapConfig from './config/mapConfig';
import './css/map.css';

const MapComponent = ({ points }) => {
  const [mapView, setMapView] = useState(null);

  useEffect(() => {
    esriConfig.apiKey = process.env.REACT_APP_ARCGIS_API_KEY;

    const map = new Map({
      basemap: mapConfig.basemap
    });

    const view = new MapView({
      container: 'map-container',
      map: map,
      center: mapConfig.center,
      zoom: mapConfig.zoom,
    });

    const graphicsLayer = new GraphicsLayer();
    map.add(graphicsLayer);

    setMapView(view);

    // Cleanup on component unmount
    return () => {
      if (view) {
        view.destroy();
      }
    };
  }, []);

  useEffect(() => {
    if (!mapView || !points) return;

    const graphicsLayer = mapView.map.findLayerById('graphicsLayer') || new GraphicsLayer({ id: 'graphicsLayer' });
    if (!mapView.map.findLayerById('graphicsLayer')) {
      mapView.map.add(graphicsLayer);
    }

    graphicsLayer.removeAll();

    points.forEach(point => {
      const { longitude, latitude, ...attributes } = point;

      const pointGraphic = new Graphic({
        geometry: {
          type: 'point',
          longitude,
          latitude
        },
        symbol: {
          type: 'simple-marker',
          color: [226, 119, 40], // Orange
          outline: { color: [255, 255, 255], width: 1 },
          size: "8px"
        },
        attributes,
        popupTemplate: {
          title: "{name}",
          content: [{
            type: "fields",
            fieldInfos: [
              { fieldName: "genus", label: "genus" },
              { fieldName: "species", label: "species" },
              { fieldName: "category", label: "category"},
              { fieldName: "description", label: "Description" },
              { fieldName: "sample_date", label: "Sample Date" },
              { fieldName: "cellcount", label: "Cell Count" },
              { fieldName: "salinity", label: "Salinity (ppt)" },
              { fieldName: "water_temp", label: "Water Temperature (°C)" },
              { fieldName: "wind_dir", label: "Wind Direction" },
              { fieldName: "wind_speed", label: "Wind Speed (km/h)" }
            ]
          }]
        }
      });

      graphicsLayer.add(pointGraphic);
    });

  }, [points, mapView]);

  return (
    <div id="map-app-content">
      <div id="map-container" style={{ height: '100%', width: '100%' }}></div>
    </div>
  );
};

export default MapComponent;
