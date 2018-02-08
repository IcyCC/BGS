define({ "api": [
  {
    "type": "POST",
    "url": "/api/v1.0/accucheks",
    "title": "添加一个新的血糖仪(json数据)",
    "group": "accucheks",
    "name": "_______",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "sn",
            "description": "<p>血糖仪sn码</p>"
          },
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "bed_id",
            "description": "<p>病床号码</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "accucheks",
            "description": "<p>返回添加血糖仪的信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"bed_id\":\"床位号\",\n    \"sn\":\"血糖仪sn码\",\n    \"url\":\"血糖仪地址\"\n}\n{\n    \"status\":\"fail\",\n    \"reason\":\"失败原因\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/accuchek.py",
    "groupTitle": "accucheks"
  },
  {
    "type": "GET",
    "url": "/api/v1.0/accucheks",
    "title": "获取所有血糖仪信息(地址栏筛选)",
    "group": "accucheks",
    "name": "_________",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "sn",
            "description": "<p>血糖仪sn码</p>"
          },
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "bed_id",
            "description": "<p>病床号码</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "accucheks",
            "description": "<p>返回所有根据条件查询到的血糖仪信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"accuncheks\":[{\n        \"url\":\"血糖仪地址\",\n        \"sn\":\"血糖仪sn码\",\n        \"bed_id\":\"床位号\"\n    }](血糖仪信息),\n    \"prev\":\"上一页地址\",\n    \"next\":\"下一页地址\",\n    \"count\":\"总数量\",\n    \"pages\":\"总页数\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/accuchek.py",
    "groupTitle": "accucheks"
  },
  {
    "type": "DELETE",
    "url": "/api/v1.0/accucheks/<int:id>",
    "title": "删除id所代表的血糖仪",
    "group": "accucheks",
    "name": "__id_______",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "id",
            "description": "<p>血糖仪id</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "accucheks",
            "description": "<p>返回被删除的血糖仪的信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"bed_id\":\"床位号\",\n    \"sn\":\"血糖仪sn码\",\n    \"url\":\"血糖仪地址\"\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "404",
            "description": "<p>对应id的血糖仪不存在</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Error-Resopnse:",
          "content": "HTTP/1.1 404 对应的血糖仪信息不存在",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/accuchek.py",
    "groupTitle": "accucheks"
  },
  {
    "type": "GET",
    "url": "/api/v1.0/accucheks/<int:id>",
    "title": "根据id获取血糖仪信息",
    "group": "accucheks",
    "name": "__id_______",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "id",
            "description": "<p>血糖仪id</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "accucheks",
            "description": "<p>返回相应血糖仪的信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"bed_id\":\"床位号\",\n    \"sn\":\"血糖仪sn码\",\n    \"url\":\"血糖仪地址\"\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "404",
            "description": "<p>对应id的血糖仪不存在</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Error-Resopnse:",
          "content": "HTTP/1.1 404 对应的血糖仪信息不存在",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/accuchek.py",
    "groupTitle": "accucheks"
  },
  {
    "type": "PUT",
    "url": "/api/v1.0/accucheks/<int:id>",
    "title": "更改id所代表的血糖仪的信息(json数据)",
    "group": "accucheks",
    "name": "__id__________",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "id",
            "description": "<p>血糖仪id</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "accucheks",
            "description": "<p>返回更改后的血糖仪的信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"bed_id\":\"床位号\",\n    \"sn\":\"血糖仪sn码\",\n    \"url\":\"血糖仪地址\"\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "404",
            "description": "<p>对应id的血糖仪不存在</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Error-Resopnse:",
          "content": "HTTP/1.1 404 对应的血糖仪信息不存在",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/accuchek.py",
    "groupTitle": "accucheks"
  },
  {
    "type": "GET",
    "url": "/api/v1.0/login",
    "title": "通过得到的账号确定密码是否正确(json数据)",
    "group": "authentication",
    "name": "_______________",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "tel",
            "description": "<p>操作者的电话号码</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "password",
            "description": "<p>操作者的密码</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "status",
            "description": "<p>返回密码的正确与否</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"status\":\"success\"\n}\n{\n    \"status\":\"fail\",\n    \"reason\":\"the password is wrong\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/authentication.py",
    "groupTitle": "authentication"
  },
  {
    "type": "GET",
    "url": "/api/v1.0/tokens",
    "title": "根据登陆的账号密码获得token",
    "group": "authentication",
    "name": "___________token",
    "parameter": {
      "fields": {
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "token",
            "description": "<p>返回相应账号的token</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"token\":token\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/authentication.py",
    "groupTitle": "authentication"
  },
  {
    "type": "POST",
    "url": "/api/v1.0/bedhistorys",
    "title": "新建床位历史信息",
    "group": "bedhistorys",
    "name": "________",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "bed_id",
            "description": "<p>床位id</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "date",
            "description": "<p>床位历史日期_日期格式(0000-00-00)</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "time",
            "description": "<p>床位历史时间_时间模式(00:00:00)</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "id_number",
            "description": "<p>医疗卡号</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "sn",
            "description": "<p>血糖仪sn码</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "bedhistorys",
            "description": "<p>返回新建的床位历史信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"url\":\"历史信息地址\",\n    \"bed_id\":\"床位号\",\n    \"time\":\"历史信息时间\",\n    \"date\":\"历史信息日期\",\n    \"sn\":\"血糖仪sn码\",\n    \"id_number\":\"医疗卡号\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/bedhistory.py",
    "groupTitle": "bedhistorys"
  },
  {
    "type": "GET",
    "url": "/api/v1.0/bedhistorys",
    "title": "获取筛选所有的床位历史信息",
    "group": "bedhistorys",
    "name": "_____________",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "bed_id",
            "description": "<p>床位id</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "date",
            "description": "<p>床位历史日期_日期格式(0000-00-00)</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "time",
            "description": "<p>床位历史时间_时间模式(00:00:00)</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "id_number",
            "description": "<p>医疗卡号</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "sn",
            "description": "<p>血糖仪sn码</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "bedhistorys",
            "description": "<p>返回筛选过的床位历史信息信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    “bedhistorys”:[{\n        \"url\":\"历史信息地址\",\n        \"bed_id\":\"床位号\",\n        \"time\":\"历史信息时间\",\n        \"date\":\"历史信息日期\",\n        \"sn\":\"血糖仪sn码\",\n        \"id_number\":\"医疗卡号\"\n    }],\n    \"prev\":\"上一页地址\",\n    \"next\":\"下一页地址\",\n    \"count\":\"总数量\",\n    \"pages\":\"总页数\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/bedhistory.py",
    "groupTitle": "bedhistorys"
  },
  {
    "type": "PUT",
    "url": "/api/v1.0/bedhistorys/<int:id>",
    "title": "更改id所代表的床位历史的信息",
    "group": "bedhistorys",
    "name": "__id___________",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "bed_id",
            "description": "<p>床位id</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "date",
            "description": "<p>床位历史日期_日期格式(0000-00-00)</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "time",
            "description": "<p>床位历史时间_时间模式(00:00:00)</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "id_number",
            "description": "<p>医疗卡号</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "sn",
            "description": "<p>血糖仪sn码</p>"
          },
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "id",
            "description": "<p>床位历史信息id</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "bedhistorys",
            "description": "<p>返回更改的床位历史信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"url\":\"历史信息地址\",\n    \"bed_id\":\"床位号\",\n    \"time\":\"历史信息时间\",\n    \"date\":\"历史信息日期\",\n    \"sn\":\"血糖仪sn码\",\n    \"id_number\":\"医疗卡号\"\n}\n不是主治医师修改\n{\n    \"status\":\"fail\",\n    \"reason\":\"no root\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/bedhistory.py",
    "groupTitle": "bedhistorys"
  },
  {
    "type": "GET",
    "url": "/api/v1.0/bedhistorys/<int:id>",
    "title": "获取id所代表的床位历史的信息",
    "group": "bedhistorys",
    "name": "__id___________",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "id",
            "description": "<p>床位历史信息id</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "bedhistorys",
            "description": "<p>返回id所代表的床位历史信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"url\":\"历史信息地址\",\n    \"bed_id\":\"床位号\",\n    \"time\":\"历史信息时间\",\n    \"date\":\"历史信息日期\",\n    \"sn\":\"血糖仪sn码\",\n    \"id_number\":\"医疗卡号\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/bedhistory.py",
    "groupTitle": "bedhistorys"
  },
  {
    "type": "DELETE",
    "url": "/api/v1.0/bedhistorys/<int:id>",
    "title": "删除id所代表的床位历史的信息",
    "group": "bedhistorys",
    "name": "__id___________",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "id",
            "description": "<p>床位历史信息id</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "bedhistorys",
            "description": "<p>返回删除的的床位历史的信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"url\":\"历史信息地址\",\n    \"bed_id\":\"床位号\",\n    \"time\":\"历史信息时间\",\n    \"date\":\"历史信息日期\",\n    \"sn\":\"血糖仪sn码\",\n    \"id_number\":\"医疗卡号\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/bedhistory.py",
    "groupTitle": "bedhistorys"
  },
  {
    "type": "POST",
    "url": "/api/v1.0/beds",
    "title": "添加新的床位信息(json数据)",
    "group": "beds",
    "name": "________",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "id_number",
            "description": "<p>医疗卡号</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "sn",
            "description": "<p>血糖仪sn码</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "beds",
            "description": "<p>返回新添加的beds信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"id_number\":\"患者医疗卡号\",\n    \"sn\":\"血糖仪sn码\",\n    \"url\":\"床位数据地址\"\n}\n病人已经被安排在其他床上\n{\n    \"status\":\"fail\",\n    \"reason\":\"the patient has been placed on the other bed\"\n}\n血糖仪被用在其他床位\n{\n    \"status\":\"fail\",\n    \"reason\":\"the accu_chek has been used on the other bed\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/beds.py",
    "groupTitle": "beds"
  },
  {
    "type": "GET",
    "url": "/api/v1.0/beds",
    "title": "获取筛选beds信息",
    "group": "beds",
    "name": "____beds__",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "id_number",
            "description": "<p>医疗卡号</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "sn",
            "description": "<p>血糖仪sn码</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "beds",
            "description": "<p>返回经过筛选的beds信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"beds\":[{\n        \"id_number\":\"患者医疗卡号\",\n        \"sn\":\"血糖仪sn码\",\n        \"url\":\"bed数据地址\"\n    }],\n    \"count\":\"总数量\",\n    \"prev\":\"上一页地址\",\n    \"next\":\"下一页地址\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/beds.py",
    "groupTitle": "beds"
  },
  {
    "type": "DELETE",
    "url": "/api/v1.0/beds/<int:id>",
    "title": "删除id所代表的床位信息",
    "group": "beds",
    "name": "__id________",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "id",
            "description": "<p>床位id</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "beds",
            "description": "<p>返回删除的beds信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"id_number\":\"患者医疗卡号\",\n    \"sn\":\"血糖仪sn码\",\n    \"url\":\"床位数据地址\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/beds.py",
    "groupTitle": "beds"
  },
  {
    "type": "PUT",
    "url": "/api/v1.0/beds/<int:id>",
    "title": "修改id所代表的床位的信息",
    "group": "beds",
    "name": "__id_________",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "id",
            "description": "<p>床位号</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "sn",
            "description": "<p>血糖仪sn码</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "id_number",
            "description": "<p>医疗卡号</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "patient_name",
            "description": "<p>病人姓名</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "sex",
            "description": "<p>病人性别</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "tel",
            "description": "<p>病人电话</p>"
          },
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "age",
            "description": "<p>病人年龄</p>"
          },
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "doctor_id",
            "description": "<p>医生id</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "beds",
            "description": "<p>返回更改后的beds信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"id_number\":\"患者医疗卡号\",\n    \"sn\":\"血糖仪sn码\",\n    \"url\":\"床位数据地址\"\n}\n病人已经被安排在其他床\n{\n    \"status\":\"fail\",\n    \"reason\":\"the patient has been placed on the other bed\"\n}\n血糖仪已经被用在其他床位\n{\n    \"status\":\"fail\",\n    \"reason\":\"the accu_chek has been used on the other bed\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/beds.py",
    "groupTitle": "beds"
  },
  {
    "type": "GET",
    "url": "/api/v1.0/beds/<int:id>/more",
    "title": "获取id所代表床位的全部信息",
    "group": "beds",
    "name": "__id__________",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "id",
            "description": "<p>床位id</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "beds",
            "description": "<p>返回id所代表床位的全部信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"bed\":{\n        \"id_number\":\"患者医疗卡号\",\n        \"sn\":\"血糖仪sn码\",\n        \"url\":\"床位信息地址\"\n    },\n    \"datas\":\"床位所有数据的信息的地址\",\n    \"patient\":{\n        \"age\":\"患者年龄\",\n        \"datas\":\"患者数据信息地址\",\n        \"doctor_id\":\"医生id\",\n        \"id_number\":\"医疗卡号\",\n        \"patient_name\":\"患者姓名\",\n        \"sex\":\"患者性别\",\n        \"tel\":\"患者手机号\",\n        \"url\":\"患者信息地址\"\n    }\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/beds.py",
    "groupTitle": "beds"
  },
  {
    "type": "GET",
    "url": "/api/v1.0/beds/<int:id>/more_data",
    "title": "获取id所代表床位的全部数据的信息",
    "group": "beds",
    "name": "__id_____________",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "id",
            "description": "<p>床位id</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "beds",
            "description": "<p>返回id所代表床位的全部数据的信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"datas\":[{\n        \"date\":\"数据创建日期\",\n        \"time\":\"数据创建时间\",\n        \"glucose\":\"血糖值\",\n        \"sn\":\"血糖仪sn码\",\n        \"patient\":\"患者信息地址\",\n        \"id_number\":\"医疗卡号\",\n        \"url\":\"数据信息地址\"\n    }],\n    \"count\":\"总数量\",\n    \"prev\":\"上一页地址\",\n    \"next\":\"下一页地址\",\n    \"pages\":\"总页数\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/beds.py",
    "groupTitle": "beds"
  },
  {
    "type": "GET",
    "url": "/api/v1.0/beds/<int:id>",
    "title": "获取id代表的beds信息",
    "group": "beds",
    "name": "__id___beds__",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "id",
            "description": "<p>bed的id</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "beds",
            "description": "<p>返回id代表的bed的数据</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"id_number\":\"患者医疗卡号\",\n    \"sn\":\"血糖仪sn码\",\n    \"url\":\"bed数据地址\",\n    \"tel\":\"患者电话\",\n    \"sex\":\"患者性别\",\n    \"patient_name\":\"患者姓名\",\n    \"doctor_id\":\"医生id\",\n    \"age\":\"患者年龄\",\n    \"current_datas\":[{\n        \"date\":\"数据日期\",\n        \"glucose\":\"血糖\",\n        \"id_number\":\"医疗卡号\",\n        \"patient\":\"患者地址\",\n        \"sn\":\"血糖仪sn码\",\n        \"time\":\"数据时间\",\n        \"url\":\"数据地址\"\n    }](最新的10个数据)\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/beds.py",
    "groupTitle": "beds"
  },
  {
    "type": "POST",
    "url": "/api/v1.0/datas/auto",
    "title": "添加数据(不用手动输入病人数据)(json数据)",
    "group": "datas",
    "name": "____",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "sn",
            "description": "<p>血糖仪sn码</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "date",
            "description": "<p>数据日期_日期格式(0000-00-00)</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "time",
            "description": "<p>数据时间_时间格式(00:00:00)</p>"
          },
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "glucose",
            "description": "<p>血糖值</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "datas",
            "description": "<p>返回新添加的数据</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"date\":\"数据添加日期\",\n    \"time\":\"数据添加时间\",\n    \"id_number\":\"医疗卡号\",\n    \"patient\":\"病人地址\",\n    \"sn\":\"血糖仪sn码\",\n    \"url\":\"数据地址\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/datas.py",
    "groupTitle": "datas"
  },
  {
    "type": "POST",
    "url": "/api/v1.0/datas/artificial",
    "title": "添加数据(不用手动输入病人数据)(json数据)",
    "group": "datas",
    "name": "____",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "id_number",
            "description": "<p>医疗卡号</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "patient_name",
            "description": "<p>病人姓名</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "sex",
            "description": "<p>病人性别</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "tel",
            "description": "<p>病人电话</p>"
          },
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "age",
            "description": "<p>病人年龄</p>"
          },
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "doctor_id",
            "description": "<p>医生id</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "sn",
            "description": "<p>血糖仪sn码</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "date",
            "description": "<p>数据日期_日期格式(0000-00-00)</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "time",
            "description": "<p>数据时间_时间格式(00:00:00)</p>"
          },
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "glucose",
            "description": "<p>血糖值</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "datas",
            "description": "<p>返回新添加的数据</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"date\":\"数据添加日期\",\n    \"time\":\"数据添加时间\",\n    \"id_number\":\"医疗卡号\",\n    \"patient\":\"病人地址\",\n    \"sn\":\"血糖仪sn码\",\n    \"url\":\"数据地址\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/datas.py",
    "groupTitle": "datas"
  },
  {
    "type": "GET",
    "url": "/api/v1.0/datas",
    "title": "获取所有数据信息",
    "group": "datas",
    "name": "________",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "sn",
            "description": "<p>血糖仪sn码</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "date",
            "description": "<p>数据日期_日期格式(0000-00-00)</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "time",
            "description": "<p>数据时间_时间格式(00:00:00)</p>"
          },
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "glucose",
            "description": "<p>血糖值</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "datas",
            "description": "<p>返回新添加的数据</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"operators\":[{\n        \"date\":\"数据添加日期\",\n        \"time\":\"数据添加时间\",\n        \"id_number\":\"医疗卡号\",\n        \"patient\":\"病人地址\",\n        \"sn\":\"血糖仪sn码\",\n        \"url\":\"数据地址\"\n    }],\n    \"count\":\"总数量\",\n    \"prev\":\"上一页地址\",\n    \"next\":\"下一页地址\".\n    \"pages\":'总页数\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/datas.py",
    "groupTitle": "datas"
  },
  {
    "type": "GET",
    "url": "/api/v1.0/datas/<int:id>",
    "title": "根据id获取数据信息",
    "group": "datas",
    "name": "__id______",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "id",
            "description": "<p>数据id</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "datas",
            "description": "<p>返回id所代表数据信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"date\":\"数据添加日期\",\n    \"time\":\"数据添加时间\",\n    \"id_number\":\"医疗卡号\",\n    \"patient\":\"病人地址\",\n    \"sn\":\"血糖仪sn码\",\n    \"url\":\"数据地址\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/datas.py",
    "groupTitle": "datas"
  },
  {
    "type": "PUT",
    "url": "/api/v1.0/datas/<int:id>",
    "title": "更改id所代表的数据的信息",
    "group": "datas",
    "name": "__id_________",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "id_number",
            "description": "<p>医疗卡号(修改病人信息时添加)</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "patient_name",
            "description": "<p>病人姓名(修改病人信息时添加)</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "sex",
            "description": "<p>病人性别(修改病人信息时添加)</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "tel",
            "description": "<p>病人电话(修改病人信息时添加)</p>"
          },
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "age",
            "description": "<p>病人年龄(修改病人信息时添加)</p>"
          },
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "doctor_id",
            "description": "<p>医生id(修改病人信息时添加)</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "sn",
            "description": "<p>血糖仪sn码</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "date",
            "description": "<p>数据日期_日期格式(0000-00-00)</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "time",
            "description": "<p>数据时间_时间格式(00:00:00)</p>"
          },
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "glucose",
            "description": "<p>血糖值</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "datas",
            "description": "<p>返回id所代表数据信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"date\":\"数据添加日期\",\n    \"time\":\"数据添加时间\",\n    \"id_number\":\"医疗卡号\",\n    \"patient\":\"病人地址\",\n    \"sn\":\"血糖仪sn码\",\n    \"url\":\"数据地址\"\n}\n不是本人主任医生修改\n{\n    \"status\":\"fail\",\n    \"reason\":\"no root\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/datas.py",
    "groupTitle": "datas"
  },
  {
    "type": "DELETE",
    "url": "/api/v1.0/datas/<int:id>",
    "title": "删除id所代表的数据的信息",
    "group": "datas",
    "name": "__id_________",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "id",
            "description": "<p>数据id</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "datas",
            "description": "<p>返回删除的数据的信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"date\":\"数据添加日期\",\n    \"time\":\"数据添加时间\",\n    \"id_number\":\"医疗卡号\",\n    \"patient\":\"病人地址\",\n    \"sn\":\"血糖仪sn码\",\n    \"url\":\"数据地址\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/datas.py",
    "groupTitle": "datas"
  },
  {
    "type": "POST",
    "url": "/api/v1.0/operators",
    "title": "新建操作者(医生)信息(json数据)",
    "group": "operators",
    "name": "_______",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "operator_name",
            "description": "<p>医生姓名</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "password",
            "description": "<p>登录密码</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "hospital",
            "description": "<p>医院名称</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "office",
            "description": "<p>科室</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "lesion",
            "description": "<p>分区</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "tel",
            "description": "<p>医生电话</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "mail",
            "description": "<p>医生邮箱</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "operators",
            "description": "<p>返回新增的医生数据</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"url\":\"医生地址\",\n    \"hospital\":\"医生医院名称\",\n    \"office\":\"医生科室\",\n    \"lesion\":\"医生分区\",\n    \"operator_name\":\"医生姓名\"\n}\n电话已经被注册\n{\n    \"status\":\"fail\",\n    \"reason\":\"the tel or the mail has been used\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/operators.py",
    "groupTitle": "operators"
  },
  {
    "type": "GET",
    "url": "/api/v1.0/operators",
    "title": "获取查询操作者(地址栏筛选)",
    "group": "operators",
    "name": "_________",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "operator_name",
            "description": "<p>医生姓名</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "hospital",
            "description": "<p>医院名称</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "office",
            "description": "<p>科室</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "lesion",
            "description": "<p>分区</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "tel",
            "description": "<p>医生电话</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "mail",
            "description": "<p>医生邮箱</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "operators",
            "description": "<p>返回新增的医生数据</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"operators\":[{\n        \"url\":\"医生地址\",\n        \"hospital\":\"医生医院名称\",\n        \"office\":\"医生科室\",\n        \"lesion\":\"医生分区\",\n        \"operator_name\":\"医生姓名\"\n    }],\n    \"count\":\"总数量\",\n    \"prev\":\"上一页地址\",\n    \"next\":\"下一页地址\",\n    \"pages\":\"总页数\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/operators.py",
    "groupTitle": "operators"
  },
  {
    "type": "GET",
    "url": "/api/v1.0/operators/now",
    "title": "返回现在操作者的信息",
    "group": "operators",
    "name": "__________",
    "parameter": {
      "fields": {
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "operators",
            "description": "<p>返回现在操作者的信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"hospital\":\"医生医院\",\n    \"lesion\":\"医生分区\",\n    \"office\":\"医生科室\",\n    \"operator_name\":\"医生姓名\",\n    \"url\":\"医生地址\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/operators.py",
    "groupTitle": "operators"
  },
  {
    "type": "GET",
    "url": "/api/v1.0/operators/now/password",
    "title": "验证现在操作者输入密码是否正确",
    "group": "operators",
    "name": "________________",
    "parameter": {
      "fields": {
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "operators",
            "description": "<p>返回现在操作者的信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"hospital\":\"医生医院\",\n    \"lesion\":\"医生分区\",\n    \"office\":\"医生科室\",\n    \"operator_name\":\"医生姓名\",\n    \"url\":\"医生地址\"\n}\n密码错误\n{\n    \"status\":\"fail\",\n    \"reason\":\"wrong password\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/operators.py",
    "groupTitle": "operators"
  },
  {
    "type": "DELETE",
    "url": "/api/v1.0/operators/<int:id>",
    "title": "根据id删除操作者",
    "group": "operators",
    "name": "__id_____",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "id",
            "description": "<p>医生id</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "operators",
            "description": "<p>返回删除的医生数据</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"hospital\":\"医生医院\",\n    \"lesion\":\"医生分区\",\n    \"office\":\"医生科室\",\n    \"operator_name\":\"医生姓名\",\n    \"url\":\"医生地址\"\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "404",
            "description": "<p>对应id的医生不存在</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Error-Resopnse:",
          "content": "HTTP/1.1 404 对应id的医生不存在",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/operators.py",
    "groupTitle": "operators"
  },
  {
    "type": "GET",
    "url": "/api/v1.0/operators/<int:id>",
    "title": "根据id查询操作者",
    "group": "operators",
    "name": "__id_____",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "id",
            "description": "<p>医生id</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "operators",
            "description": "<p>返回新增的医生数据</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"hospital\":\"医生医院\",\n    \"lesion\":\"医生分区\",\n    \"office\":\"医生科室\",\n    \"operator_name\":\"医生姓名\",\n    \"url\":\"医生地址\"\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "404",
            "description": "<p>对应id的医生不存在</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Error-Resopnse:",
          "content": "HTTP/1.1 404 对应id的医生不存在",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/operators.py",
    "groupTitle": "operators"
  },
  {
    "type": "PUT",
    "url": "/api/v1.0/operators",
    "title": "根据id修改操作者信息(json数据)",
    "group": "operators",
    "name": "__id_______",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "id",
            "description": "<p>医生id</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "operators",
            "description": "<p>返回修改后的的医生数据</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"hospital\":\"医生医院\",\n    \"lesion\":\"医生分区\",\n    \"office\":\"医生科室\",\n    \"operator_name\":\"医生姓名\",\n    \"url\":\"医生地址\"\n}\n电话已被用于注册\n{\n    \"status\":\"fail\",\n    \"reason\":\"the tel or the mail has been used\"    \n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "404",
            "description": "<p>对应id的医生不存在</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Error-Resopnse:",
          "content": "HTTP/1.1 404 对应id的医生不存在",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/operators.py",
    "groupTitle": "operators"
  },
  {
    "type": "POST",
    "url": "/api/v1.0/patients",
    "title": "新建病人信息(json数据)",
    "group": "patients",
    "name": "______",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "id_number",
            "description": "<p>医保卡号</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "tel",
            "description": "<p>病人电话号码</p>"
          },
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "doctor_id",
            "description": "<p>医生号码</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "sex",
            "description": "<p>患者性别</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "patient_name",
            "description": "<p>患者姓名</p>"
          },
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "age",
            "description": "<p>患者年龄</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "patients",
            "description": "<p>返回新病人信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"url\": \"病人信息地址\",\n    \"patient_name\":\"病人姓名\",\n    \"sex\":\"病人性别\",\n    \"tel\":\"病人电话\",\n    \"age\":\"病人年龄\",\n    \"doctor_id\":\"医生号码\",\n    \"id_number\":\"医保卡号\",\n    \"datas\":\"病人数据地址\"\n}\n医保卡号如果被注册过了\n{\n    \"status\":\"fail\",\n    \"reason\":\"the id_number has been used\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/patients.py",
    "groupTitle": "patients"
  },
  {
    "type": "GET",
    "url": "/api/v1.0/patients",
    "title": "获取所有病人数据信息(地址栏筛选)",
    "group": "patients",
    "name": "________",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "id_number",
            "description": "<p>医保卡号</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "tel",
            "description": "<p>病人电话号码</p>"
          },
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "doctor_id",
            "description": "<p>医生号码</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "sex",
            "description": "<p>患者性别</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "patient_name",
            "description": "<p>患者姓名</p>"
          },
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "age",
            "description": "<p>患者年龄</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "patients",
            "description": "<p>返回查询到的病人信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"patients\":[{\n        \"url\": \"病人信息地址\",\n        \"patient_name\":\"病人姓名\",\n        \"sex\":\"病人性别\",\n        \"tel\":\"病人电话\",\n        \"age\":\"病人年龄\",\n        \"doctor_id\":\"医生号码\",\n        \"id_number\":\"医保卡号\",\n        \"datas\":\"病人数据地址\"    \n    }],\n    \"prev\":\"上一页\",\n    \"next\":\"下一页\",\n    \"count\":\"总数量\".\n    \"pages\":\"总页数\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/patients.py",
    "groupTitle": "patients"
  },
  {
    "type": "GET",
    "url": "/api/v1.0/patients/get-from-id",
    "title": "根据医疗卡号获取病人信息",
    "group": "patients",
    "name": "____________",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "id_number",
            "description": "<p>医疗卡号</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "patients",
            "description": "<p>返回根据医疗卡号获取的病人信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"url\": \"病人信息地址\",\n    \"patient_name\":\"病人姓名\",\n    \"sex\":\"病人性别\",\n    \"tel\":\"病人电话\",\n    \"age\":\"病人年龄\",\n    \"doctor_id\":\"医生号码\",\n    \"id_number\":\"医保卡号\",\n    \"datas\":\"病人数据地址\"    \n}\n这个医疗卡号没有注册过\n{\n    \"status\":\"fail\",\n    \"reason\":\"the patient does not exist\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/patients.py",
    "groupTitle": "patients"
  },
  {
    "type": "GET",
    "url": "/api/v1.0/patients/<int:id>",
    "title": "根据id获取病人信息",
    "group": "patients",
    "name": "__id______",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "id",
            "description": "<p>病人id</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "patients",
            "description": "<p>返回id所代表的病人信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"url\": \"病人信息地址\",\n    \"patient_name\":\"病人姓名\",\n    \"sex\":\"病人性别\",\n    \"tel\":\"病人电话\",\n    \"age\":\"病人年龄\",\n    \"doctor_id\":\"医生号码\",\n    \"id_number\":\"医保卡号\",\n    \"datas\":\"病人数据地址\"    \n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "404",
            "description": "<p>对应id的病人不存在</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Error-Resopnse:",
          "content": "HTTP/1.1 404 对应的病人信息不存在",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/patients.py",
    "groupTitle": "patients"
  },
  {
    "type": "PUT",
    "url": "/api/v1.0/patients/<int:id>",
    "title": "修改id代表的病人信息(json数据)",
    "group": "patients",
    "name": "__id_______",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "id",
            "description": "<p>病人id</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "id_number",
            "description": "<p>医保卡号</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "tel",
            "description": "<p>病人电话号码</p>"
          },
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "doctor_id",
            "description": "<p>医生号码</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "sex",
            "description": "<p>患者性别</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "patient_name",
            "description": "<p>患者姓名</p>"
          },
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "age",
            "description": "<p>患者年龄</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "patients",
            "description": "<p>返回修改后的病人信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"url\": \"病人信息地址\",\n    \"patient_name\":\"病人姓名\",\n    \"sex\":\"病人性别\",\n    \"tel\":\"病人电话\",\n    \"age\":\"病人年龄\",\n    \"doctor_id\":\"医生号码\",\n    \"id_number\":\"医保卡号\",\n    \"datas\":\"病人数据地址\"    \n}\n医保卡号已注册\n{\n    \"status\":\"fail\",\n    \"reason\":\"the id_number has been used\"\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "404",
            "description": "<p>对应id的病人不存在</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Error-Resopnse:",
          "content": "HTTP/1.1 404 对应的病人信息不存在",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/patients.py",
    "groupTitle": "patients"
  },
  {
    "type": "DELETE",
    "url": "/api/v1.0/patients/<int:id>",
    "title": "删除id所代表的病人信息",
    "group": "patients",
    "name": "__id________",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "id",
            "description": "<p>病人id</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "patients",
            "description": "<p>返回删除后的病人信息</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"url\": \"病人信息地址\",\n    \"patient_name\":\"病人姓名\",\n    \"sex\":\"病人性别\",\n    \"tel\":\"病人电话\",\n    \"age\":\"病人年龄\",\n    \"doctor_id\":\"医生号码\",\n    \"id_number\":\"医保卡号\",\n    \"datas\":\"病人数据地址\"    \n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "404",
            "description": "<p>对应id的病人不存在</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Error-Resopnse:",
          "content": "HTTP/1.1 404 对应的病人信息不存在",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/patients.py",
    "groupTitle": "patients"
  },
  {
    "type": "GET",
    "url": "/api/v1.0/patients/<int:id>/datas",
    "title": "获取id所代表的病人的数据",
    "group": "patients",
    "name": "__id_________",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "id",
            "description": "<p>病人id</p>"
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "datas",
            "description": "<p>返回id所表示病人的数据</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"datas\":[{\n        \"date\":\"数据日期\",\n        \"glucose\":\"血糖值\",\n        \"id_number\":\"医疗卡号\",\n        \"patient\":\"病人地址\",\n        \"sn\":\"血糖仪sn码\",\n        \"url\":\"数据地址\",\n        \"time\":\"数据时间\"\n    }]，\n    \"prev\":\"上一页地址\",\n    \"next\":\"下一页地址\",\n    \"count\":\"总数量\",\n    \"pages\":\"总页数\"    \n}\n没有数据\n{\n    \"status\":\"fail\",\n    \"reason\":\"there is no data\"\n}",
          "type": "json"
        }
      ]
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "404",
            "description": "<p>对应id的病人不存在</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Error-Resopnse:",
          "content": "HTTP/1.1 404 对应的病人信息不存在",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/patients.py",
    "groupTitle": "patients"
  },
  {
    "type": "GET",
    "url": "/api/v1.0/patients/history",
    "title": "获取病人历史信息(浏览器栏筛选)",
    "group": "patients",
    "name": "__id_________",
    "parameter": {
      "fields": {
        "params": [
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "id_number",
            "description": "<p>医疗卡号</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "patient_name",
            "description": "<p>病人名字</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "sex",
            "description": "<p>病人性别</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "tel",
            "description": "<p>病人电话</p>"
          },
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "age",
            "description": "<p>病人年龄</p>"
          },
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "max_age",
            "description": "<p>病人最大年龄</p>"
          },
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "min_age",
            "description": "<p>病人最小年龄</p>"
          },
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "max_glucose",
            "description": "<p>病人最大血糖值</p>"
          },
          {
            "group": "params",
            "type": "Number",
            "optional": false,
            "field": "min_glucose",
            "description": "<p>病人最小血糖值</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "begin_time",
            "description": "<p>开始时间_时间格式（00:00:00）</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "end_time",
            "description": "<p>结束时间</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "begin_date",
            "description": "<p>开始日期_日期格式（0000-00-00）</p>"
          },
          {
            "group": "params",
            "type": "String",
            "optional": false,
            "field": "end_date",
            "description": ""
          }
        ],
        "Login": [
          {
            "group": "Login",
            "type": "String",
            "optional": false,
            "field": "login",
            "description": "<p>登录才可以访问</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Array",
            "optional": false,
            "field": "datas",
            "description": "<p>返回筛选过的数据</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "HTTP/1.1 200 OK\n{\n    \"datas\":[{\n        \"date\":\"数据日期\",\n        \"glucose\":\"血糖值\",\n        \"id_number\":\"医疗卡号\",\n        \"patient\":\"病人地址\",\n        \"sn\":\"血糖仪sn码\",\n        \"url\":\"数据地址\",\n        \"time\":\"数据时间\"\n    }],\n    \"prev\":\"上一页地址\",\n    \"next\":\"下一页地址\",\n    \"count\":\"总数量\",\n    \"pages\":\"总页数\"    \n}\n没有数据\n{\n    \"status\":\"fail\",\n    \"reason\":\"there is no data\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "app/api_1_0/patients.py",
    "groupTitle": "patients"
  }
] });
