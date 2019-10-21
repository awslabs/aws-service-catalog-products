import {Injectable} from '@angular/core';
import {ProductInfo, ProductLaunchList} from "../_models";
import {BehaviorSubject, Observable} from "rxjs";
import {HttpClient} from "@angular/common/http";
import {environment} from "../../environments/environment";

@Injectable({
    providedIn: 'root'
})
export class ListLaunchService {

    list_launches: Observable<ProductInfo[]>;
    baseUrl: string = `${environment.apiUrl}/assets/list-launches.json`;
    private _list_launches: BehaviorSubject<ProductInfo[]>;
    private dataStore: {  // This is where we will store our data in memory
        list_launches: ProductInfo[];
    };

    constructor(private http: HttpClient) {
        this.dataStore = {list_launches: []};
        this._list_launches = <BehaviorSubject<ProductInfo[]>>new BehaviorSubject([]);
        this.list_launches = this._list_launches.asObservable();
    }

    loadAll() {
        let product_array: ProductInfo[];
        return this.http.get<ProductLaunchList[]>(`${this.baseUrl}`)
            .subscribe(
                data => {
                    console.log('Loading the data from JSON....');
                    console.log(data);
                    product_array = Object.keys(data).map(function (key) {
                        return data[key];
                    });
                    console.log('Data converted to a collection....');
                    console.log(product_array);
                    this.dataStore.list_launches = product_array;
                    this._list_launches.next(Object.assign({}, this.dataStore).list_launches);
                }, error => console.log('Failed to load status.', error)
            )
    }
}
