import React, { useEffect, useState } from 'react';
import Map from '@arcgis/core/Map';
import MapView from '@arcgis/core/views/MapView';
import Graphic from '@arcgis/core/Graphic';
import GraphicsLayer from '@arcgis/core/layers/GraphicsLayer';
import esriConfig from '@arcgis/core/config';
import  SimpleMarkerSymbol  from '@arcgis/core/symbols/SimpleMarkerSymbol';
import  SimpleLineSymbol  from '@arcgis/core/symbols/SimpleLineSymbol';
import Color from '@arcgis/core/Color';

import mapConfig from './config/mapConfig';
import './css/map.css';
import {drawBoundingBoxes} from "./helper/bbox";
import bbox from "./helper/bbox.json";
import categoryMapping from "./config/categoryMapping"
const MapComponent = ({ points, area, isPredict }) => {
  const [mapView, setMapView] = useState(null);
  
  const getSymbol = (category) => {
    let symbol;

    switch (category) {
      case "not observed":
        symbol = new SimpleMarkerSymbol({
          style: "x",
          size: 6,
          color: new Color([255, 255, 255, 1]),
          outline: { 
            color: new Color([0, 0, 0]),
            width: 1
          }
        });
        break;
      case "very low":
        symbol = new SimpleMarkerSymbol({
          style: "circle",
          size: 6,
          color: new Color([255, 255, 255, 1]),
          outline: {
            color: new Color([0, 0, 0]),
            width: 0.75
          }
        });
        break;
      case "low":
        symbol = new SimpleMarkerSymbol({
          style: "circle",
          size: 10,
          color: new Color([255, 255, 0, 1]),
          outline: {
            color: new Color([0, 0, 0]),
            width: 1
          }
        });
        break;
      case "medium":
        symbol = new SimpleMarkerSymbol({
          style: "circle",
          size: 14,
          color: new Color([255, 125, 0, 1]),
          outline: {
            color: new Color([0, 0, 0]),
            width: 1
          }
        });
        break;
      case "high":
        symbol = new SimpleMarkerSymbol({
          style: "circle",
          size: 18,
          color: new Color([255, 0, 0, 1]),
          outline: {
            color: new Color([0, 0, 0]),
            width: 1
          }
        });
        break;
      // Default case to handle unexpected categories
      default:
        symbol = new SimpleMarkerSymbol({
          style: "circle",
          size: 6,
          color: new Color([200, 200, 200, 1]),
          outline: {
            color: new Color([0, 0, 0]),
            width: 1
          }
        });
    }
    return symbol;

  };
  const getPredictSymbol = (category) => {
    let symbol;
    const categoryStr = String(category);  // or category.toString();

    switch (categoryStr) {
      case '0':
        symbol = new SimpleMarkerSymbol({
          style: "x",
          size: 6,
          color: new Color([255, 255, 255, 1]),
          outline: { 
            color: new Color([0, 0, 0]),
            width: 1
          }
        });
        break;
      case '1':
        symbol = new SimpleMarkerSymbol({
          style: "circle",
          size: 6,
          color: new Color([255, 255, 255, 1]),
          outline: {
            color: new Color([0, 0, 0]),
            width: 0.75
          }
        });
        break;
      case '2':
        symbol = new SimpleMarkerSymbol({
          style: "circle",
          size: 6,
          color: new Color([255, 255, 0, 1]),
          outline: {
            color: new Color([0, 0, 0]),
            width: 1
          }
        });
        break;
      case '3':
        symbol = new SimpleMarkerSymbol({
          style: "circle",
          size: 6,
          color: new Color([255, 125, 0, 1]),
          outline: {
            color: new Color([0, 0, 0]),
            width: 1
          }
        });
        break;
      case '4':
        symbol = new SimpleMarkerSymbol({
          style: "circle",
          size: 6,
          color: new Color([255, 0, 0, 1]),
          outline: {
            color: new Color([0, 0, 0]),
            width: 1
          }
        });
        break;
      // Default case to handle unexpected categories
      default:
        symbol = new SimpleMarkerSymbol({
          style: "circle",
          size: 6,
          color: new Color([200, 200, 200, 1]),
          outline: {
            color: new Color([0, 0, 0]),
            width: 1
          }
        });
    }
    return symbol;

  };




  const createAndAddGraphic = (point) => {
    const { longitude, latitude, category, ...otherAttributes } = point;
    const attributes = { ...otherAttributes, category, longitude, latitude };
    const symbol = getSymbol(category);
    
    const pointGraphic = new Graphic({
      geometry: {
        type: 'point',
        longitude,
        latitude
      },
      symbol: symbol,

      attributes,
      popupTemplate: {
        title: "{description}",
        content: [{
          type: "fields",
          fieldInfos: [
            { fieldName: "longitude", label: "longitude" },
            { fieldName: "latitude", label: "latitude" },
            { fieldName: "genus", label: "genus" },
            { fieldName: "species", label: "species" },
            { fieldName: "category", label: "category"},
            { fieldName: "description", label: "Description" },
            { fieldName: "sample_datetime", label: "Sample Date" },
            { fieldName: "cellcount", label: "Cell Count(cells/L)" },
            { fieldName: "salinity", label: "Salinity (ppt)" },
            { fieldName: "water_temp", label: "Water Temperature (°C)" },
            { fieldName: "wind_dir", label: "Wind Direction" },
            { fieldName: "wind_speed", label: "Wind Speed (miles/h)" }
          ]
        }]
      }
    });

    mapView.map.findLayerById('graphicsLayer').add(pointGraphic);
  };

  function getCategoryText(numericCategory) {
    
    return categoryMapping[numericCategory] || 'Unknown'; // Default to 'Unknown' if no mapping exists
  }

  function aggregatePointsByLocation(points) {
    // console.log('aggregate');
    // console.log(points);
    const groupedByLocation = points.reduce((acc, point) => {
      const coordsKey = `${point.latitude}_${point.longitude}`;
      if (!acc[coordsKey]) {
        acc[coordsKey] = {
          latitude: point.latitude,
          longitude: point.longitude,
          predictions: []
        };
      }
      acc[coordsKey].predictions.push({
        datetime: point.datetime,
        predict_category: point.predict_category,
        predict_category_txt: getCategoryText(point.predict_category),
        salinity: point.salinity,
        water_temp: point.water_temp,
        wind_dir: point.wind_dir,
        wind_speed: point.wind_speed
      });
      return acc;
    }, {});
  
    return Object.values(groupedByLocation).map(location => {
      const totalCategory = location.predictions.reduce((acc, pred) => {
        return acc + parseInt(pred.predict_category, 10);  // Use parseInt for integers, parseFloat for decimal numbers
      }, 0);
      const avgCategory = Math.round(totalCategory / location.predictions.length);

      return {
          ...location,
          avg_category: avgCategory,
          predictions: location.predictions.sort((a, b) => new Date(a.datetime) - new Date(b.datetime))
      };
    });
  }



  const createAndAddGraphicPredictionAgg = (locationWithPredictions) => {
    const { longitude, latitude, predictions, avg_category} = locationWithPredictions;
  
    // Construct the HTML content for the popup
    let popupContent = `<table>
      <tr><th>Date</th><th>Predict Category</th><th>Salinity</th><th>Water Temp</th><th>Wind Dir</th><th>Wind Speed</th></tr>`;
    predictions.forEach(pred => {
      popupContent += `<tr>
        <td>${new Date(pred.datetime).toLocaleDateString()}</td>
        <td>${pred.predict_category_txt}</td>
        <td>${pred.salinity}</td>
        <td>${pred.water_temp}</td>
        <td>${pred.wind_dir}</td>
        <td>${pred.wind_speed}</td>
      </tr>`;
    });
    popupContent += `</table>`;
  
    const pointGraphic = new Graphic({
      geometry: {
        type: 'point',
        longitude,
        latitude
      },
      symbol: getPredictSymbol(avg_category), // Assuming the first prediction has the symbol
      attributes: locationWithPredictions,
      popupTemplate: {
        title: "Predictions for {latitude}, {longitude}, {avg_category}",
        content: popupContent
      }
    });
    mapView.map.findLayerById('graphicsLayer').add(pointGraphic);
  };


  const createAndAddGraphicPrediction=(point)=>{
    const { longitude, latitude, predict_category, ...otherAttributes } = point;
    
    const predictCategoryText = getCategoryText(predict_category);

    const attributes = { 
      ...otherAttributes, 
      predict_category,
      predict_category_txt: predictCategoryText, // Use the transformed category text here
      longitude, 
      latitude 
    };
    
    const symbol = getPredictSymbol(predict_category);

    const pointGraphic = new Graphic({
      geometry: {
        type: 'point',
        longitude,
        latitude
      },
      symbol: symbol,

      attributes,
      popupTemplate: {
        title: "{description}",
        content: [{
          type: "fields",
          fieldInfos: [
            { fieldName: "longitude", label: "longitude" },
            { fieldName: "latitude", label: "latitude" },
            { fieldName: "predict_category_txt", label: "Predict_category"},
            { fieldName: "description", label: "Description" },
            { fieldName: "datetime", label: "Sample Date" },
            { fieldName: "salinity", label: "Salinity (ppt)" },
            { fieldName: "water_temp", label: "Water Temperature (°C)" },
            { fieldName: "wind_dir", label: "Wind Direction" },
            { fieldName: "wind_speed", label: "Wind Speed (miles/h)" }
          ]
        }]
      }
    });
    mapView.map.findLayerById('graphicsLayer').add(pointGraphic);

  };


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
    const graphicsLayer = new GraphicsLayer({ id: 'graphicsLayer' });
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

    if (area) {
      drawBoundingBoxes(graphicsLayer, [{ coordinates: area.coordinates }]);
    }
    if (isPredict){
      // points.forEach(createAndAddGraphicPrediction);
      const aggregatedPoints = aggregatePointsByLocation(points);
      console.log(aggregatedPoints);
      aggregatedPoints.forEach(createAndAddGraphicPredictionAgg);


    }
    else{
      points.forEach(createAndAddGraphic);

    }

  }, [points, mapView, area]);

  return (
    <div id="map-app-content">
      <div id="map-container" style={{ height: '100%', width: '100%' }}></div>
    </div>
  );
};

export default MapComponent;
