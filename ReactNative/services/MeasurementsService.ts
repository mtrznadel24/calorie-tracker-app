import {api} from "@/api/axiosInstance";
import {Weight, WeightCreate} from "@/services/weightService";

export interface Measurement {
  id: number;
  date: string;
  weight: Weight | null;
  neck: number | null;
  biceps: number | null;
  chest: number | null;
  waist: number | null;
  hips: number | null;
  thighs: number | null;
  calves: number | null;
}

export interface MeasurementCreate {
  weight?: WeightCreate | null;
  neck?: number | null;
  biceps?: number | null;
  chest?: number | null;
  waist?: number | null;
  hips?: number | null;
  thighs?: number | null;
  calves?: number | null;
}

const MeasurementsService = {
  async addMeasurement(data: MeasurementCreate) {
    const response = await api.post("/measurements", data);
    return response.data;
  },

  async getUserMeasurements() {
    const response = await api.get("/measurements");
    return response.data;
  },

  async getLatestMeasurement() {
    const response = await api.get("/measurements/latest")
    return response.data;
  },

  async deleteMeasurement(id: number) {
    await api.delete(`measurements/${id}`)
  }
};

export default MeasurementsService;