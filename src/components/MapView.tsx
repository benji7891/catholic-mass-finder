import { useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import type { Church } from '../types';
import 'leaflet/dist/leaflet.css';

// Fix default marker icons (Leaflet + bundlers issue)
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

const selectedIcon = new L.Icon({
  iconUrl: markerIcon,
  iconRetinaUrl: markerIcon2x,
  shadowUrl: markerShadow,
  iconSize: [30, 46],
  iconAnchor: [15, 46],
  popupAnchor: [0, -46],
  shadowSize: [41, 41],
  className: 'selected-marker',
});

interface MapViewProps {
  parishes: Church[];
  center: [number, number] | null;
  selectedId: number | null;
  onSelect: (church: Church) => void;
}

function MapUpdater({ center, parishes }: { center: [number, number] | null; parishes: Church[] }) {
  const map = useMap();
  const hasSet = useRef(false);

  useEffect(() => {
    if (parishes.length > 0) {
      const bounds = L.latLngBounds(
        parishes.map((p) => [p.latitude, p.longitude] as [number, number])
      );
      map.fitBounds(bounds, { padding: [40, 40], maxZoom: 13 });
      hasSet.current = true;
    } else if (center && !hasSet.current) {
      map.setView(center, 12);
    }
  }, [center, parishes, map]);

  return null;
}

export default function MapView({ parishes, center, selectedId, onSelect }: MapViewProps) {
  const defaultCenter: [number, number] = center ?? [39.8283, -98.5795]; // Center of US

  return (
    <MapContainer
      center={defaultCenter}
      zoom={center ? 12 : 4}
      className="h-full w-full rounded-lg"
      scrollWheelZoom={true}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <MapUpdater center={center} parishes={parishes} />
      {parishes.map((church) => (
        <Marker
          key={church.id}
          position={[church.latitude, church.longitude]}
          icon={church.id === selectedId ? selectedIcon : new L.Icon.Default()}
          eventHandlers={{
            click: () => onSelect(church),
          }}
        >
          <Popup>
            <div className="text-sm">
              <strong>{church.name}</strong>
              <br />
              {church.address}, {church.city}
              {church.distance != null && (
                <>
                  <br />
                  <span className="text-gray-500">{church.distance.toFixed(1)} mi</span>
                </>
              )}
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}
