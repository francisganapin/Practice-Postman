from flask import Flask,request,jsonify
import pandas as pd


app = Flask(__name__)
df = pd.read_csv("data.csv")


@app.route('/data',methods=['GET'])
def get_data():
    return jsonify(df.to_dict(orient='records'))

@app.route('/data/<int:row_id>',methods=['GET'])
def get_row(row_id):
    row = df[df['id'] == row_id]
    if not row.empty:
        return jsonify(row.iloc[0].to_dict())
    else:
        return jsonify({'error':'No data found with That id'}),404
    
@app.route('/filter',methods=['GET'])
def filter_data():
    city = request.args.get('city','').lower()
    filtered_df = df[df['city'].str.lower() == city]
    if not filtered_df.empty:
        return jsonify(filtered_df.to_dict(orient='records'))
    else:
        return jsonify({'message':'No data Found for this City'})
    
if __name__ == '__main__':
    app.run(debug=True)