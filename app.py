from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, SelectField
from os import path
import pandas as pd
import numpy as np
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
bootstrap = Bootstrap(app)

script_dir = path.dirname(path.abspath(__file__))


class customerForm(FlaskForm):

    a = SelectField('2-methylbuta-1,3-diene', choices=[('2', 'Produced'), ('1', 'Increased'), ('0', 'No Change'), ('-1', 'Decreased')])           
    b = SelectField('hexanal', choices=[('2', 'Produced'), ('1', 'Increased'), ('0', 'No Change'), ('-1', 'Decreased')])    
    c = SelectField('heptanal', choices=[('2', 'Produced'), ('1', 'Increased'), ('0', 'No Change'), ('-1', 'Decreased')])
    d = SelectField('butan-2-one', choices=[('2', 'Produced'), ('1', 'Increased'), ('0', 'No Change'), ('-1', 'Decreased')])           
    e = SelectField('2-methylpentane', choices=[('2', 'Produced'), ('1', 'Increased'), ('0', 'No Change'), ('-1', 'Decreased')])           

def predict_disease(A,B,C,D,a,b,c,d,e):
    count = 0
    poss = []
    if (a==-1)&(b==-1)&(c==-1)&(d==-1)&(e==-1): return 'Probability of following cancers ','None'
    for i in [a,b,c,d,e]:
        if i==2:
            if A[0,count]==1: poss.append('Lung')
            if B[0,count]==1: poss.append('Gastric and esophageal')
            if C[0,count]==1: poss.append('Breast')
            if D[0,count]==1: poss.append('Colorectal')
        elif i==1:
            if A[1,count]==1: poss.append('Lung')
            if B[1,count]==1: poss.append('Gastric and esophageal')
            if C[1,count]==1: poss.append('Breast')
            if D[1,count]==1: poss.append('Colorectal')
        elif i==0:
            if A[2,count]==1: poss.append('Lung')
            if B[2,count]==1: poss.append('Gastric and esophageal')
            if C[2,count]==1: poss.append('Breast')
            if D[2,count]==1: poss.append('Colorectal')
        elif i==-1:
            if A[3,count]==1: poss.append('Lung')
            if B[3,count]==1: poss.append('Gastric and esophageal')
            if C[3,count]==1: poss.append('Breast')
            if D[3,count]==1: poss.append('Colorectal')
        count+=1
    
    if poss == []: return 'Probability of following cancers ','None'
    else:   return 'Probability of following cancers ',list(set(poss)) 
   
    
@app.route ("/result",methods=['GET','POST'])
def result():
    form = customerForm()
    if request.method == 'POST':
        
        try:
            a = form.a.data
        except:
            a = -1
            
        try:
            b = form.b.data
        except:
            b = -1
            
        try:
            c = form.b.data
        except:
            c = -1
            
        try:
            d = form.c.data
        except:
            d = -1
            
        try:
            e = form.d.data
        except:
            e = -1
            
        data = pd.read_csv('voccancer.csv')
        data.loc[data.Trend=='decrease','Trend'] = 'Decrease'
        data.loc[data.Trend=='increase','Trend'] = 'Increase'
        data.loc[data.Trend=='Decrease?','Trend'] = 'Decrease'
        data.loc[:,'Trend_val'] = data.Trend.map({'Increase':1, 'Decrease':-1, '-': 0, 'Produced':2, 'Metabolized':3})
        
        breath_data = data[data.TypeofControl=='Breath samples from healthy individuals']
        
        breath_req = breath_data[(breath_data.Compound == 'hexanal')|(breath_data.Compound == 'butan-2-one')|(breath_data.Compound == '2-methylbuta-1,3-diene')|(breath_data.Compound == '2-methylpentane')|(breath_data.Compound == 'heptanal')][['TypeofCancer','Compound','Trend_val']]
        
        A = np.zeros((len(data.Trend.value_counts()),5))
        B = np.zeros((len(data.Trend.value_counts()),5))
        C = np.zeros((len(data.Trend.value_counts()),5))
        D = np.zeros((len(data.Trend.value_counts()),5))
        
        breath_req1 = breath_req[breath_req.TypeofCancer=='Lung']
        for i in range(len(breath_req1)):
            if (breath_req1.iloc[i,1]=='2-methylbuta-1,3-diene')&((breath_req.iloc[i,2]==2)): A[0,0]=1
            elif (breath_req1.iloc[i,1]=='hexanal')&((breath_req.iloc[i,2]==2)): A[0,1]=1
            elif (breath_req1.iloc[i,1]=='heptanal')&((breath_req.iloc[i,2]==2)): A[0,2]=1
            elif (breath_req1.iloc[i,1]=='butan-2-one')&((breath_req.iloc[i,2]==2)): A[0,3]=1
            elif (breath_req1.iloc[i,1]=='2-methylpentane')&((breath_req.iloc[i,2]==2)): A[0,4]=1
            elif (breath_req1.iloc[i,1]=='2-methylbuta-1,3-diene')&((breath_req.iloc[i,2]==1)): A[1,0]=1
            elif (breath_req1.iloc[i,1]=='hexanal')&((breath_req.iloc[i,2]==1)): A[1,1]=1
            elif (breath_req1.iloc[i,1]=='heptanal')&((breath_req.iloc[i,2]==1)): A[1,2]=1
            elif (breath_req1.iloc[i,1]=='butan-2-one')&((breath_req.iloc[i,2]==1)): A[1,3]=1
            elif (breath_req1.iloc[i,1]=='2-methylpentane')&((breath_req.iloc[i,2]==1)): A[1,4]=1
            elif (breath_req1.iloc[i,1]=='2-methylbuta-1,3-diene')&((breath_req.iloc[i,2]==0)): A[2,0]=1
            elif (breath_req1.iloc[i,1]=='hexanal')&((breath_req.iloc[i,2]==0)): A[2,1]=1
            elif (breath_req1.iloc[i,1]=='heptanal')&((breath_req.iloc[i,2]==0)): A[2,2]=1
            elif (breath_req1.iloc[i,1]=='butan-2-one')&((breath_req.iloc[i,2]==0)): A[2,3]=1
            elif (breath_req1.iloc[i,1]=='2-methylpentane')&((breath_req.iloc[i,2]==0)): A[2,4]=1
            elif (breath_req1.iloc[i,1]=='2-methylbuta-1,3-diene')&((breath_req.iloc[i,2]==-1)): A[3,0]=1
            elif (breath_req1.iloc[i,1]=='hexanal')&((breath_req.iloc[i,2]==-1)): A[3,1]=1
            elif (breath_req1.iloc[i,1]=='heptanal')&((breath_req.iloc[i,2]==-1)): A[3,2]=1
            elif (breath_req1.iloc[i,1]=='butan-2-one')&((breath_req.iloc[i,2]==-1)): A[3,3]=1
            elif (breath_req1.iloc[i,1]=='2-methylpentane')&((breath_req.iloc[i,2]==-1)): A[3,4]=1
            
        breath_req2 = breath_req[breath_req.TypeofCancer=='Gastric and esophageal']

        for i in range(len(breath_req2)):
            if (breath_req2.iloc[i,1]=='2-methylbuta-1,3-diene')&((breath_req.iloc[i,2]==2)): B[0,0]=1
            elif (breath_req2.iloc[i,1]=='hexanal')&((breath_req.iloc[i,2]==2)): B[0,1]=1
            elif (breath_req2.iloc[i,1]=='heptanal')&((breath_req.iloc[i,2]==2)): B[0,2]=1
            elif (breath_req2.iloc[i,1]=='butan-2-one')&((breath_req.iloc[i,2]==2)): B[0,3]=1
            elif (breath_req2.iloc[i,1]=='2-methylpentane')&((breath_req.iloc[i,2]==2)): B[0,4]=1
            elif (breath_req2.iloc[i,1]=='2-methylbuta-1,3-diene')&((breath_req.iloc[i,2]==1)): B[1,0]=1
            elif (breath_req2.iloc[i,1]=='hexanal')&((breath_req.iloc[i,2]==1)): B[1,1]=1
            elif (breath_req2.iloc[i,1]=='heptanal')&((breath_req.iloc[i,2]==1)): B[1,2]=1
            elif (breath_req2.iloc[i,1]=='butan-2-one')&((breath_req.iloc[i,2]==1)): B[1,3]=1
            elif (breath_req2.iloc[i,1]=='2-methylpentane')&((breath_req.iloc[i,2]==1)): B[1,4]=1
            elif (breath_req2.iloc[i,1]=='2-methylbuta-1,3-diene')&((breath_req.iloc[i,2]==0)): B[2,0]=1
            elif (breath_req2.iloc[i,1]=='hexanal')&((breath_req.iloc[i,2]==0)): B[2,1]=1
            elif (breath_req2.iloc[i,1]=='heptanal')&((breath_req.iloc[i,2]==0)): B[2,2]=1
            elif (breath_req2.iloc[i,1]=='butan-2-one')&((breath_req.iloc[i,2]==0)): B[2,3]=1
            elif (breath_req2.iloc[i,1]=='2-methylpentane')&((breath_req.iloc[i,2]==0)): B[2,4]=1
            elif (breath_req2.iloc[i,1]=='2-methylbuta-1,3-diene')&((breath_req.iloc[i,2]==-1)): B[3,0]=1
            elif (breath_req2.iloc[i,1]=='hexanal')&((breath_req.iloc[i,2]==-1)): B[3,1]=1
            elif (breath_req2.iloc[i,1]=='heptanal')&((breath_req.iloc[i,2]==-1)): B[3,2]=1
            elif (breath_req2.iloc[i,1]=='butan-2-one')&((breath_req.iloc[i,2]==-1)): B[3,3]=1
            elif (breath_req2.iloc[i,1]=='2-methylpentane')&((breath_req.iloc[i,2]==-1)): B[3,4]=1
            
        breath_req3 = breath_req[breath_req.TypeofCancer=='Breast']

        for i in range(len(breath_req3)):
            if (breath_req3.iloc[i,1]=='2-methylbuta-1,3-diene')&((breath_req.iloc[i,2]==2)): C[0,0]=1
            elif (breath_req3.iloc[i,1]=='hexanal')&((breath_req.iloc[i,2]==2)): C[0,1]=1
            elif (breath_req3.iloc[i,1]=='heptanal')&((breath_req.iloc[i,2]==2)): C[0,2]=1
            elif (breath_req3.iloc[i,1]=='butan-2-one')&((breath_req.iloc[i,2]==2)): C[0,3]=1
            elif (breath_req3.iloc[i,1]=='2-methylpentane')&((breath_req.iloc[i,2]==2)): C[0,4]=1
            elif (breath_req3.iloc[i,1]=='2-methylbuta-1,3-diene')&((breath_req.iloc[i,2]==1)): C[1,0]=1
            elif (breath_req3.iloc[i,1]=='hexanal')&((breath_req.iloc[i,2]==1)): C[1,1]=1
            elif (breath_req3.iloc[i,1]=='heptanal')&((breath_req.iloc[i,2]==1)): C[1,2]=1
            elif (breath_req3.iloc[i,1]=='butan-2-one')&((breath_req.iloc[i,2]==1)): C[1,3]=1
            elif (breath_req3.iloc[i,1]=='2-methylpentane')&((breath_req.iloc[i,2]==1)): C[1,4]=1
            elif (breath_req3.iloc[i,1]=='2-methylbuta-1,3-diene')&((breath_req.iloc[i,2]==0)): C[2,0]=1
            elif (breath_req3.iloc[i,1]=='hexanal')&((breath_req.iloc[i,2]==0)): C[2,1]=1
            elif (breath_req3.iloc[i,1]=='heptanal')&((breath_req.iloc[i,2]==0)): C[2,2]=1
            elif (breath_req3.iloc[i,1]=='butan-2-one')&((breath_req.iloc[i,2]==0)): C[2,3]=1
            elif (breath_req3.iloc[i,1]=='2-methylpentane')&((breath_req.iloc[i,2]==0)): C[2,4]=1
            elif (breath_req3.iloc[i,1]=='2-methylbuta-1,3-diene')&((breath_req.iloc[i,2]==-1)): C[3,0]=1
            elif (breath_req3.iloc[i,1]=='hexanal')&((breath_req.iloc[i,2]==-1)): C[3,1]=1
            elif (breath_req3.iloc[i,1]=='heptanal')&((breath_req.iloc[i,2]==-1)): C[3,2]=1
            elif (breath_req3.iloc[i,1]=='butan-2-one')&((breath_req.iloc[i,2]==-1)): C[3,3]=1
            elif (breath_req3.iloc[i,1]=='2-methylpentane')&((breath_req.iloc[i,2]==-1)): C[3,4]=1
            
        breath_req4 = breath_req[breath_req.TypeofCancer=='Colorectal']

        for i in range(len(breath_req4)):
            if (breath_req4.iloc[i,1]=='2-methylbuta-1,3-diene')&((breath_req.iloc[i,2]==2)): D[0,0]=1
            elif (breath_req4.iloc[i,1]=='hexanal')&((breath_req.iloc[i,2]==2)): D[0,1]=1
            elif (breath_req4.iloc[i,1]=='heptanal')&((breath_req.iloc[i,2]==2)): D[0,2]=1
            elif (breath_req4.iloc[i,1]=='butan-2-one')&((breath_req.iloc[i,2]==2)): D[0,3]=1
            elif (breath_req4.iloc[i,1]=='2-methylpentane')&((breath_req.iloc[i,2]==2)): D[0,4]=1
            elif (breath_req4.iloc[i,1]=='2-methylbuta-1,3-diene')&((breath_req.iloc[i,2]==1)): D[1,0]=1
            elif (breath_req4.iloc[i,1]=='hexanal')&((breath_req.iloc[i,2]==1)): D[1,1]=1
            elif (breath_req4.iloc[i,1]=='heptanal')&((breath_req.iloc[i,2]==1)): D[1,2]=1
            elif (breath_req4.iloc[i,1]=='butan-2-one')&((breath_req.iloc[i,2]==1)): D[1,3]=1
            elif (breath_req4.iloc[i,1]=='2-methylpentane')&((breath_req.iloc[i,2]==1)): D[1,4]=1
            elif (breath_req4.iloc[i,1]=='2-methylbuta-1,3-diene')&((breath_req.iloc[i,2]==0)): D[2,0]=1
            elif (breath_req4.iloc[i,1]=='hexanal')&((breath_req.iloc[i,2]==0)): D[2,1]=1
            elif (breath_req4.iloc[i,1]=='heptanal')&((breath_req.iloc[i,2]==0)): D[2,2]=1
            elif (breath_req4.iloc[i,1]=='butan-2-one')&((breath_req.iloc[i,2]==0)): D[2,3]=1
            elif (breath_req4.iloc[i,1]=='2-methylpentane')&((breath_req.iloc[i,2]==0)): D[2,4]=1
            elif (breath_req4.iloc[i,1]=='2-methylbuta-1,3-diene')&((breath_req.iloc[i,2]==-1)): D[3,0]=1
            elif (breath_req4.iloc[i,1]=='hexanal')&((breath_req.iloc[i,2]==-1)): D[3,1]=1
            elif (breath_req4.iloc[i,1]=='heptanal')&((breath_req.iloc[i,2]==-1)): D[3,2]=1
            elif (breath_req4.iloc[i,1]=='butan-2-one')&((breath_req.iloc[i,2]==-1)): D[3,3]=1
            elif (breath_req4.iloc[i,1]=='2-methylpentane')&((breath_req.iloc[i,2]==-1)): D[3,4]=1
            
        x,y = predict_disease(A,B,C,D,int(a),int(b),int(c),int(d),int(e))    
        
        return {x:y}
            
        
                
    return 'No disease'

@app.route ("/")
def index():
    form = customerForm()
    return render_template("index.html",form= form)
    



if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)

#from flask import Flask, render_template
#from flask_wtf import FlaskForm
#from wtforms import StringField, PasswordField
#from wtforms.validators import InputRequired, Length, AnyOf
#
#app = Flask(__name__)
#app.config['SECRET_KEY'] = 'Thisisasecret!'
#
#class LoginForm(FlaskForm):
#    username = StringField('username', validators=[InputRequired('A username is required!'), Length(min=5, max=10, message='Must be between 5 and 10 characters.')])
#    password = PasswordField('password', validators=[InputRequired('Password is required!'), AnyOf(values=['password', 'secret'])])
#
#@app.route('/form', methods=['GET', 'POST'])
#def form():
#    form = LoginForm()
#
#    if form.validate_on_submit():
#        return '<h1>The username is {}. The password is {}.'.format(form.username.data, form.password.data)
#    return render_template('form.html', form=form)
#
#if __name__ == '__main__':
#    from waitress import serve
#    serve(app, host="0.0.0.0", port=5050)