import {Injectable} from '@angular/core';
import {PipelineInfo} from "../_models";
import {BehaviorSubject, Observable} from "rxjs";
import {HttpClient} from "@angular/common/http";
import {environment} from "../../environments/environment";

@Injectable({
    providedIn: 'root'
})
export class PipelineStatusService {

    pipelines: Observable<PipelineInfo[]>;
    baseUrl: string = `${environment.apiUrl}/assets/show-pipelines.json`;
    private _pipelines: BehaviorSubject<PipelineInfo[]>;
    private dataStore: {  // This is where we will store our data in memory
        pipelines: PipelineInfo[];
    };

    constructor(private http: HttpClient) {
        this.dataStore = {pipelines: []};
        this._pipelines = <BehaviorSubject<PipelineInfo[]>>new BehaviorSubject([]);
        this.pipelines = this._pipelines.asObservable();
    }

    loadAll() {
        let pipeline_array: PipelineInfo[];
        return this.http.get<PipelineInfo[]>(`${this.baseUrl}`)
            .subscribe(
                data => {
                    console.log('Loading the data from JSON....');
                    console.log(data);
                    pipeline_array = Object.keys(data).map(function (key) {
                        return data[key];
                    });
                    console.log('Data converted to a collection....');
                    console.log(pipeline_array);
                    this.dataStore.pipelines = pipeline_array;
                    this._pipelines.next(Object.assign({}, this.dataStore).pipelines);
                }, error => console.log('Failed to load status.', error)
            )
    }
}
